import re
from decimal import Decimal

def normalize_money_add(text):
    text = str(text)
    money_re = re.compile('^\d[\d\s\.\,]+\d')
    match = money_re.search(text)
    if match:
        money_str = match.group(0)
        money_str = re.sub(r'\s', '', money_str)
        money_str = re.sub(',', '.', money_str)
        return Decimal(money_str)
    return Decimal(0)

def normalize_money(text):
    text = str(text)
    if text and re.sub(r'[^\d.]', '', text):
        return Decimal(re.sub(r'[^\d.]', '', text))
    return Decimal(0)

def normalize_money_desc(text):
    text = str(text)
    return re.sub(r'\)|\(', '', text)

def calc_money_diff(pd_row):
    money_add = normalize_money_add(pd_row[5])
    money_dec = normalize_money(pd_row[4])
    return money_dec - money_add

def shorten_name(long_name):
   ministries_short_name = {
       'Министерство внутренних дел РФ': 'МВД России',
       'Министерство экономического развития РФ': 'Минэкономразвития России',
       'Министерство финансов РФ': 'Минфин России',
       'Министерство промышленности и торговли РФ': 'Минпромторг России',
       'Министерство энергетики РФ': 'Минэнерго России',
       'Министерство здравоохранения РФ ': 'Минздрав России',
       'Министерство сельского хозяйства РФ': 'Минсельхоз России',
       'Министерство транспорта РФ': 'Минтранс России',
       'Министерство Российской Федерации по развитию Дальнего Востока и Арктики': 'Минвостокразвития России',
       'Министерство Российской Федерации по развитию Дальнего Востока и Арктики (Минвостокразвития России)': 'Минвостокразвития России',
       'Министерство цифрового развития, связи и массовых коммуникаций Российской Федерации': 'Минцифры России',
       'Министерство культуры РФ': 'Минкультуры России',
       'Министерство природных ресурсов и экологии РФ': 'Минприроды России',
       'Министерство труда и социальной защиты РФ': 'Минтруд России',
       'Министерство спорта РФ': 'Минспорт России',
       'Министерство строительства и жилищно-коммунального хозяйства РФ': 'Минстрой России',
       'Министерство юстиции РФ': 'Минюст России',
       'Министерство науки и высшего образования РФ': 'Минобрнауки России',
       'Министерство иностранных дел РФ': 'МИД России',
       'Министерство просвещения РФ': 'Минпросвещения России',
       'Министерство здравоохранения РФ': 'Минздрав России'
    }  
   return ministries_short_name.get(long_name, long_name)

#стандартизированные названия
positions_dict = {
    r'первыйзаместитель\w*министра': 'первый заместитель федерального министра',
    r'заместитель\w*министра': 'заместитель федерального министра',
    r'помощник\w*министра': 'помощник федерального министра',
    r'советник\w*министра': 'советник федерального министра',
    r'заместител(ь|я)(руководител[ья]|начальника*|директорa*)\w*службы\w*министерства': 'заместитель руководителя службы федерального министерства',
    r'(руководител[ья]|начальника*|директорa*)\w*службы\w*министерства': 'руководитель службы федерального министерства',
    r'заместител[ья](руководител[ья]|начальника*|директорa*)\w*аппарата\w*министра': 'заместитель руководителя аппарата федерального министра',
    r'(руководител[ья]|начальника*|директорa*)\w*аппарата\w*министра': 'руководитель аппарата федерального министра',
    r'заместител[ья](руководител[ья]|начальника*|директорa*)\w*главногоуправления': 'заместитель руководителя главного управления',
    r'(руководител[ья]|начальника*|директорa*)\w*главногоуправления': 'руководитель главного управления',
    r'заместител[ья](руководител[ья]|начальника*|директорa*)\w*территориальногоуправления': 'заместитель руководителя территориального управления',
    r'(руководител[ья]|начальника*|директорa*)\w*территориальногоуправления': 'руководитель территориального управления',
    r'заместител[ья](руководител[ья]|начальника*|директорa*)\w*управления': 'заместитель руководителя управления',
    r'заместител[ья](руководител[ья]|начальника*|директорa*)\w*умвд': 'заместитель руководителя управления',
    r'(руководител[ья]|начальника*|директорa*)\w*управления': 'руководитель управления',
    r'(руководител[ья]|начальника*|директорa*)\w*умвд': 'руководитель управления',
    r'заместител[ья](руководител[ья]|начальника*|директорa*)\w*департамент': 'заместитель руководителя департамента',
    r'(руководител[ья]|начальника*|директорa*)\w*департамент': 'руководитель департамента',
    r'заместител[ья](руководител[ья]|начальника*|директорa*)\w*отделав\w*департамент': 'заместитель руководитель отдела в департаменте',
    r'(руководител[ья]|начальника*|директорa*)\w*отделав\w*департамент': 'руководитель отдела в департаменте',
    r'заместител[ья](руководител[ья]|начальника*|директорa*)\w*отделавслужбе\w*министерства': 'заместитель руководителя отдела в службе федерального министерства',
    r'(руководител[ья]|начальника*|директорa*)отделавслужбе\w*министерства': 'руководитель отдела в службе федерального министерства',
    r'заместител[ья](руководител[ья]|начальника*|директорa*)\wотдел': 'заместитель руководителя отдела',
    r'(руководител[ья]|начальника*|директорa*)\w*отдел': 'руководитель отдела',
    r'заместител[ья](руководител[ья]|начальника*|директорa*)\wтерриториальногооргана': 'заместитель руководителя территориального органа',
    r'(руководител[ья]|начальника*|директорa*)\w*территориальногооргана': 'руководитель территориального органа',
    r'заместител[ья](руководител[ья]|начальника*|директорa*)\wаппарата': 'заместитель руководителя аппарата',
    r'(руководител[ья]|начальника*|директорa*)\w*аппарата': 'руководитель аппарата',
    'ведущийсоветник': 'ведущий советник',
    'советник': 'советник ',
    'ведущийконсультант': 'ведущий консультант',
    'консультант': 'консультант',
    'главныйспециалистэксперт': 'главный специалист-эксперт',
    'главныйспециалист': 'главный специалист',
    'ведущийспециалистэксперт': 'ведущий специалист-эксперт',
    'специалистэксперт': 'специалист-эксперт',
    'ведущийспециалист2разряда': 'ведущий специалист 2 разряда',
    'старшийспециалист1разряда': 'старший специалист 1 разряда',
    'старшийспециалист2разряда': 'старший специалист 2 разряда',
    'старшийспециалист3разряда': 'старший специалист 3 разряда',
    'специалист1разряда': 'специалист 1 разряда',
    'специалист2разряда': 'специалист 2 разряда',
    'референтотдела':'референт отдела',
    'референтдепартамента':'референт департамента',
    'референт':'референт',
    'министр':'министр'
    }

#категории
category_dict = {
    'начальник отдела' : 'руководители / специалисты', 
    'заместитель директора департамента' : 'руководители',
    'референт' : 'специалисты',
    'директор департамента' : 'руководители',
    'заместитель начальника отдела' : 'руководители / специалисты',
    'заместитель федерального министра' : 'руководители',
    'советник' : 'специалисты',
    'консультант' : 'специалисты',
    'помощник федерального министра' : 'помощники (советники)',
    'советник федерального министра' : 'помощники (советники)',
    'ведущий советник' : 'специалисты',
    'главный специалист-эксперт' : 'специалисты',
    'ведущий консультант' : 'специалисты',
    'ведущий специалист-эксперт' : 'специалисты',
    'первый заместитель федерального министра' : 'руководители',
    'специалист-эксперт' : 'специалисты',
    'специалист 1 разряда' : 'обеспечивающие специалисты',
    'ведущий специалист 2 разряда' : 'обеспечивающие специалисты',
    'старший специалист 1 разряда' : 'обеспечивающие специалисты',
    'специалист 2 разряда' : 'обеспечивающие специалисты', 
    'заместитель руководителя аппарата федерального министра' : 'руководители',
    'старший специалист 3 разряда' : 'обеспечивающие специалисты',
    'руководитель аппарата федерального министра' : 'руководители'}

#группы
group_dict = {
    'начальник отдела' : 'главная', 
    'заместитель директора департамента' : 'высшая',
    'референт' : 'главная',
    'директор департамента' : 'высшая',
    'заместитель начальника отдела' : 'главная / ведущая',
    'заместитель федерального министра' : 'высшая',
    'советник' : 'ведущая',
    'консультант' : 'ведущая',
    'помощник федерального министра' : 'высшая',
    'советник федерального министра' : 'высшая',
    'ведущий советник' : 'ведущая',
    'главный специалист-эксперт' : 'старшая',
    'ведущий консультант' : 'ведущая',
    'ведущий специалист-эксперт' : 'старшая',
    'первый заместитель федерального министра' : 'высшая',
    'специалист-эксперт' : 'старшая',
    'специалист 1 разряда' : 'старшая',
    'ведущий специалист 2 разряда' : 'ведущая',
    'старший специалист 1 разряда' : 'старшая',
    'специалист 2 разряда' : 'младшая', 
    'заместитель руководителя аппарата федерального министра' : 'высшая',
    'старший специалист 3 разряда' : 'старшая',
    'руководитель аппарата федерального министра' : 'высшая'}

def find_category(name):
    name_key = re.sub(r'[^\w|\d]', '', name.lower())
    for key, value in positions_dict.items():
        if re.search(key, name_key):
            return value 
    else:
        return None

