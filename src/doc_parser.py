 # -*- coding: utf-8 -*-
import xlrd
import zipfile
import csv
import itertools
import re
from decimal import Decimal 
from bs4 import BeautifulSoup
import locale

from src import settings, utils

class Item():
    def __init__(self,t_type,own_type = "Собственность"):
        self.type = t_type
        self.own_type = own_type
        self.proportion = None
        self.meters = None#Оставим строкой
        self.country = None
        self.car = None
        self.errors = []

        if not self.type:
            self.add_error("Ячейка типа недвижимости пуста.")
        if not self.own_type:
            self.add_error("Ячейка вида владения недвижимостью пуста.")
        
    @classmethod
    def new_flat(cls,t_type):
        #недвижимость по умолчанию создается в пользование
        #если есть вид собственности он добавится позднее
        return cls(t_type,"Пользование")

    @classmethod
    def new_car(cls,car_str):
        new_car = cls("транспорт")
        new_car.car = car_str
        return new_car

    def add_error(self,error_str):
        self.errors.append(error_str)
        Row_Info.error_counter+=1


    def add_owntype(self,own_type_str):
        if own_type_str is None:
            self.add_error(f'Ячейка типа собственности пуста')
            self.own_type = ""
            return

        #в own_type могут быть пропорции собственности
        #могут встречаться дроби вида ½ ¼ ¾
        own_type_str = re.sub("½","1/2",own_type_str)
        own_type_str = re.sub("¼","1/4",own_type_str)
        own_type_str = re.sub("¾","3/4",own_type_str)
        proportion = re.findall(r'\d+/\d+',own_type_str)
        if proportion:
            own_type_str = re.sub(proportion[-1],"",own_type_str)
            self.proportion = proportion[-1]
            own_type_str = re.sub(r",?\s*дол(ей|я|и)\s*$", "",own_type_str)

        self.own_type = own_type_str.strip()
        

    def add_meters(self, meters):
        #meters_str = 12 или 12,34 или 12.34

        if meters is None:
            self.add_error(f'Ячейка квадратных метров пуста')
            return
        elif isinstance(meters, str):
            #Уберем пробелы везде и точки и запятые в конце
            meters_str = re.sub(r"\s|(\,\s+$)|(\.\s+$)","",meters)
            if re.fullmatch(r'(\d+)|(\d+,\d+)|(\d+.\d+)',meters_str):
                meters_str = re.sub(",",".",meters_str)
                #print("money_str : "+money_str)
                meters_dec = Decimal(meters_str)
                
            else:
                self.add_error(f'Некорректно указаны квадратные метры "{meters}"')
                return

        else:
            meters_dec = Decimal(meters)

        self.meters = locale.format("%.1f", meters_dec)

    def add_country(self, country_str):
        if country_str is None:
            self.add_error(f'Ячейка страны пуста')
            return
        self.country = country_str.strip()


    def get_fields():
        fields = []
        fields.append("type")
        fields.append("own_type")
        fields.append("proportion")
        fields.append("meters")
        fields.append("country")
        fields.append("car")
        return fields


    def get_entry(self):
        entry = dict.fromkeys(Item.get_fields())
        entry['type'] = utils.clear_text_from_noise(self.type)
        entry['own_type'] = utils.clear_text_from_noise(self.own_type)
        entry['proportion'] = self.proportion
        entry['meters'] = self.meters
        entry['country'] = utils.clear_text_from_noise(self.country)
        entry['car'] = utils.clear_text_from_noise(self.car)
        return entry

    def get_empty():
        entry = []
        entry.append(None)#type
        entry.append(None)#own_type
        entry.append(None)#proportion
        entry.append(None)#meters
        entry.append(None)#country
        entry.append(None)#car
        return entry

class Person():

    clerk_iter = itertools.count(start = 1)
    child_iter = itertools.count(start = 2)
    _child_list = []

    def __init__(self):
        self.id = str(next(Person.clerk_iter))
        self.name = ""
        self.position = ""
        self.family = "Чиновник"
        self.money = ""
        self.money_desc = ""
        self.source = ""
        self.errors = []
        Person._child_list = []
        Person.child_iter = itertools.count(start = 2)
    

    def add_error(self,error_str):
        self.errors.append(error_str)
        Row_Info.error_counter+=1


    def restart_clerk_counter():
        Person.clerk_iter = itertools.count(start = 1)

    def make_relative(self,relative_str):
        #для родственников
        if relative_str == 'Cупруг':# С латинской С
            relative_str = 'Супруг'

        if relative_str in Person._child_list:
            self.family = relative_str+" "+str(next(Person.child_iter))
        else:
            self.family = relative_str
            Person._child_list.append(relative_str)
        self.money = ""
        self.money_desc = ""
        self.source = ""
        self.errors = []

    def add_money(self,money):
        #Строка вида 1234567,89 (с запятой)
        #А иногда вида 1234567.89 (с точкой)
        #А иногда вида 1234 567,89 (с пробелами)
        
        if not money:
            #бедняжечка
            return

        if isinstance(money, str):
            pattern = re.compile(r'(\s|\.|,|\d)+')
            if not pattern.match(money):
                self.add_error(f'Некорректно записан декларированный доход "{money}"')
                return
            money_str = pattern.match(money).group()
            self.money_desc = re.sub(money_str,"",money)
            #Уберем пробелы везде и запятые в конце
            money_str = re.sub(r"\s|(\,\s+$)","",money_str)
        
            if re.fullmatch(r'(\d+)|(\d+,\d+)|(\d+\.\d+)',money_str):
                #Если в сумме больше двух знаков после запятой, записываем в ошибки
                if re.fullmatch(r'(\d+,\d{3,})|(\d+\.\d{3,})',money_str):
                    self.add_error(f'Некорректно записан декларированный доход "{money}"')
                
                money_str = re.sub(",",".",money_str)
                #print("money_str : "+money_str)
                money_dec = Decimal(money_str)
                
            else:
                self.add_error(f'Некорректно записан декларированный доход "{money}"')
                return

        else:
            money_dec = Decimal(money)

        self.money = locale.currency(money_dec,symbol="",grouping = True)
    
    def add_source(self,source_str):
        self.source = source_str


    def get_fields():
        fields = []
        fields.append("id")
        fields.append("name")
        fields.append("position")
        fields.append("family")
        fields.append("money")
        fields.append("money_desc")
        fields.append("source")
        return fields


    def get_entry(self):
        entry = dict.fromkeys(Person.get_fields())
        entry['id'] = self.id
        entry['name'] = utils.clear_text_from_noise(self.name)
        entry['position'] = utils.clear_text_from_noise(self.position)
        entry['family'] = utils.clear_text_from_noise(self.family)
        entry['money'] = self.money
        entry['money_desc'] = self.money_desc
        entry['source'] = utils.clear_text_from_noise(self.source)
        return entry


#Информация из одной строки
class Row_Info():
    curr_person = None
    empty_value_pattern = ""
    state_name = ""
    year = ""
    doc_caption = ""
    error_counter = 0


    def __init__(self):
        self.own_flats = []
        self.rent_flats = []
        self.cars = []
        self.errors = []
        self.its_addstr = True


    def set_empty_value_pattern(pattern_str):
        Row_Info.empty_value_pattern = re.compile(r'[\s\[\]'+pattern_str+r']*')

    
    def set_file_info(state_name,year,doc_caption,file_url):
        Row_Info.state_name = state_name
        Row_Info.year = year
        Row_Info.doc_caption = doc_caption
        Row_Info.file_url = file_url

    
    def add_error(self,error_str):
        self.errors.append(error_str)
        Row_Info.error_counter+=1

    def restart_error_counter():
        Row_Info.error_counter = 0


    def value_not_empty(value):
        #print(str(value))
        if value is None:
            return False
        elif (isinstance(value, list) 
            and Row_Info.empty_value_pattern.fullmatch("".join(map(str,value)))):
            return False
        elif Row_Info.empty_value_pattern.fullmatch(str(value)):
            return False
        else:
            return True

    def bring_value(value):
        if isinstance(value, list):
            #Лист параграфов
            value = " ".join(par_str for par_str in value if 
                Row_Info.value_not_empty(par_str))

        if not Row_Info.value_not_empty(value):
            return ""
        else:
            return value


    def remove_empty(cell_list):
        if isinstance(cell_list, list):
            cell_list = list(filter(Row_Info.value_not_empty,cell_list))

        return cell_list


    def split_entry(value):
        #Разбивка содержимого ячейки по пробелам
        if value == '':
            return '', ''
        if isinstance(value, str):
            splited = value.split(' ')
            splited = list(a for a in splited if a!='')
            if len(splited) == 0:
                return '', ''
            elif len(splited) == 1:
                return splited[0], ''
            else:
                return splited[0], " ".join(splited[1:])
            
        else:
            return value, ""



    def its_new_person(self,name,position,num_pp):
        #print("num_pp : "+str(num_pp))
        num_pattern = re.compile(r'\s*\d+\.*\d*\s*')
        if isinstance(num_pp, (int, float, complex)):
            its_clerk = True
        elif isinstance(num_pp, str) and num_pattern.fullmatch(num_pp):
            its_clerk = True
        elif isinstance(num_pp, str):
            its_clerk = False
        elif isinstance(num_pp, list) and num_pattern.fullmatch("".join(map(str, num_pp))):
            its_clerk = True
        elif isinstance(num_pp, list):
            its_clerk = False
        elif num_pp is None:
            #Номера ПП нет будем определять по имени
            
            #relative_pattern = re.compile(r'супруг|несовершеннолетн')
            #its_clerk = not bool(relative_pattern.match(name))

            #Есть должность = чиновник
            if (position 
                and not re.search(r'(cупруг|несовершеннолетний)',name,re.IGNORECASE)):
                its_clerk = True
            else:
                its_clerk = False

        else:
            print(f'Проверить номер ПП для {name}')
            its_clerk = False

        self.its_addstr = False
        if not its_clerk and position:
            self.add_error('Должность у члена семьи')
        elif its_clerk and not position:
            self.add_error('Отсутствие должности у чиновника')


        if its_clerk:
            Row_Info.curr_person = Person()
            Row_Info.curr_person.name = name
            Row_Info.curr_person.position = position
        else:
            Row_Info.curr_person.make_relative(name)

    def add_position(self, position):
        #Для должности записаной в несколько строк
        Row_Info.curr_person.position += " " +position
    
    
    def add_money(self,money):
        #print(f'money : {money}')
        money = Row_Info.bring_value(money)
        if not self.its_addstr:
            Row_Info.curr_person.add_money(money)
        elif money:
            self.add_error(f'Доход в дополнительной строке : {money}')

            
    def add_source(self,source):
        if not self.its_addstr:
            Row_Info.curr_person.add_source(Row_Info.bring_value(source))


    def add_ownflat(self,type_str,owntype_str,meters_str,country_str):
        type_str = Row_Info.bring_value(type_str)
        owntype_str = Row_Info.bring_value(owntype_str)
        meters_str = Row_Info.bring_value(meters_str)
        country_str = Row_Info.bring_value(country_str)

        if not (type_str or owntype_str or meters_str or country_str):
            #Если ничего не заполнено, квартиры нет
            return

        own_flat = Item.new_flat(t_type = type_str)
        own_flat.add_country(country_str)
        own_flat.add_owntype(owntype_str)
        own_flat.add_meters(meters_str)
        
        self.own_flats.append(own_flat)


    def add_rentflat(self,type_str,meters_str,country_str):
        type_str = Row_Info.bring_value(type_str)
        meters_str = Row_Info.bring_value(meters_str)
        country_str = Row_Info.bring_value(country_str)

        if not (type_str or meters_str):
            #Если ничего не заполнено, 
            #Или заполнена только страна
            #квартиры нет
            return

        rent_flat = Item.new_flat(t_type = type_str)
        rent_flat.add_country(country_str)
        rent_flat.add_meters(meters_str)
        
        self.rent_flats.append(rent_flat)


    def add_car(self,car_entry):
        car_str = Row_Info.bring_value(car_entry)
        if car_str:
            self.cars.append(Item.new_car(car_str))


    def get_fields():
        fields = Person.get_fields() + Item.get_fields()
        
        if settings.ADD_ERR:
            fields+=['errors',]
        
        if settings.ADD_FILEDESC:
            fields+=['state_name','year']

        if settings.ADD_DOCCAPTION:
            fields+=['doc_caption',]

        if settings.ADD_FILEURL:
            fields+=['file_url',]

        return fields

    
    def get_entryes(self):
        entry = dict.fromkeys(Row_Info.get_fields())
        
        if 'errors' in entry:
            entry['errors'] = ""+"; ".join(self.errors+Row_Info.curr_person.errors)

        if 'state_name' in entry:
            entry['state_name'] = Row_Info.state_name

        if 'year' in entry:
            entry['year'] = Row_Info.year

        if 'doc_caption' in entry:
            entry['doc_caption'] = Row_Info.doc_caption

        if 'file_url' in entry:
            entry['file_url'] = Row_Info.file_url

        entry.update(Row_Info.curr_person.get_entry())
        
        if not self.own_flats and not self.rent_flats and not self.cars:
                    # если чиновник без ничего
            
            yield entry

        for item in (self.own_flats+self.rent_flats+self.cars):
            item_dict = dict()
            item_dict.update(entry)
            item_dict.update(item.get_entry())
            
            if 'errors' in item_dict:
                item_dict['errors'] += "; ".join(item.errors)
            

            yield item_dict


def decompose_one_row(row_values,doc_structure):
    #print('row_values : '+str(row_values))
    
    if doc_structure.transform_function is not None:
        row_values = doc_structure.transform_function(row_values)

    #print('row_values : '+str(row_values))
    
    #Если это набор пустых колонок
    if not any(Row_Info.value_not_empty(s) for s in row_values):
        return []
    
    row_info = Row_Info()

    #В одной колонке значения двух колонок через пробел
    for split_cell in doc_structure.split_cells:
        part_a = row_values[split_cell]
        if isinstance(part_a, list):
            part_b = []
            for ind_a, val_a in enumerate(part_a):
                try:
                    val_a, val_b = Row_Info.split_entry(val_a)
                except ValueError as err:
                    row_info.add_error(str(err))
                    val_b = ''
                part_a[ind_a] = val_a
                part_b.append(val_b)
        else:
            try:
                part_a, part_b = Row_Info.split_entry(part_a)
            except ValueError as err:
                row_info.add_error(str(err))
                part_b = ''
        
        row_values[split_cell] = part_a
        row_values.insert(split_cell+1,part_b)


    cell_diff = len(row_values)-doc_structure.cells_count
    if cell_diff>0 and cell_diff not in doc_structure.extra_cells_intheend:
        print(str(row_values))
        raise ValueError(f'Ошибка парсинга. Слишком много ячеек в строке : {len(row_values)}')

    #В doc->docx документах объединение ячеек конвертируется как строка с меньшим их количеством 
    if len(row_values)<4:
        #это заголовок или разделитель
        return []
    elif cell_diff<0:
        row_info.add_error('Меньшее количество ячеек в строке. Проверьте правильность дополнения.')
        while len(row_values) < doc_structure.cells_count:
            row_values.insert(doc_structure.insert_cells_ind,"")


    num_pp  = doc_structure.get_cell('num_pp',row_values)
    name = Row_Info.bring_value(doc_structure.get_cell('name',row_values))
    position = Row_Info.bring_value(doc_structure.get_cell('position',row_values))

    #В некоторых файлах степень родства отдельной колонкой
    family = doc_structure.get_cell('family',row_values)
    if Row_Info.value_not_empty(family):
        #print(f'name : {name}')
        #print(f'family : {family}')
        #print(f'position : {position}')
        name = Row_Info.bring_value(family)
        position = ''

    if bool(name):
        row_info.its_new_person(name,position,num_pp)
    elif position:
        #В некоторых файлах должность пишется в несколько строк
        row_info.add_position(position)


    row_info.add_money(row_values[doc_structure.money])
    row_info.add_source(row_values[doc_structure.source])
    
    #*****own flat *****
    own_flat_type = Row_Info.remove_empty(row_values[doc_structure.ownflats_type])
    own_flat_owntype = Row_Info.remove_empty(row_values[doc_structure.ownflats_owntype])
    own_flat_meters = Row_Info.remove_empty(row_values[doc_structure.ownflats_meters])
    own_flat_country = Row_Info.remove_empty(row_values[doc_structure.ownflats_country])
        
    
    if doc_structure.list_in_cell or doc_structure.multi_row_value:
        #Если не хватает значений в колонке own_flat_country, наверное там Россия
        max_len = max(len(own_flat_type),len(own_flat_owntype),len(own_flat_meters),len(own_flat_country))
        own_flat_country += ['Россия']*(max_len - len(own_flat_country))
        
        while (len(own_flat_type)>0
            and len(own_flat_owntype)>0
            and len(own_flat_meters)>0
            and len(own_flat_country)>0
            ):
            row_info.add_ownflat(
                own_flat_type.pop(0),
                own_flat_owntype.pop(0),
                own_flat_meters.pop(0),
                own_flat_country.pop(0)
                )
        #После того как добавили все совпадающее, остались куски
        extra_lines = "; ".join(own_flat_type+own_flat_owntype+own_flat_meters+own_flat_country)
        if extra_lines:
            row_info.add_error("Не совпадает количество значений в колонках"
            +f" недвижимости в собственности. Остались лишние значения : {extra_lines}")

        
    else:
        row_info.add_ownflat(
            own_flat_type,
            own_flat_owntype,
            own_flat_meters,
            own_flat_country
            )

    #*****rent flat *****
    rent_flat_type = Row_Info.remove_empty(row_values[doc_structure.rentflats_type])
    rent_flat_meters = Row_Info.remove_empty(row_values[doc_structure.rentflats_meters])
    rent_flat_country = Row_Info.remove_empty(row_values[doc_structure.rentflats_country])
        
    
    if doc_structure.list_in_cell or doc_structure.multi_row_value:
        #print(f'rent_flat_type : {rent_flat_type}')
        #print(f'rent_flat_meters : {rent_flat_meters}')
        #print(f'rent_flat_country : {rent_flat_country}')
        #Если не хватает значений в колонке rent_flat_country, наверное там Россия
        
        max_len = max(len(rent_flat_type),len(rent_flat_meters),len(rent_flat_country))
        rent_flat_country += ['Россия']*(max_len - len(rent_flat_country))
        
        while (len(rent_flat_type)>0
            and len(rent_flat_meters)>0
            and len(rent_flat_country)>0
            ):
            row_info.add_rentflat(
                rent_flat_type.pop(0),
                rent_flat_meters.pop(0),
                rent_flat_country.pop(0)
                )
        #После того как добавили все совпадающее, остались куски
        extra_lines = "; ".join(rent_flat_type+rent_flat_meters+rent_flat_country)
        if extra_lines:
            row_info.add_error("Не совпадает количество значений в колонках"
            +f" недвижимости в пользовании. Остались лишние значения : {extra_lines}")

    else:
        row_info.add_rentflat(
            rent_flat_type,
            rent_flat_meters,
            rent_flat_country
            )

    #***** car *****
    cars = Row_Info.remove_empty(row_values[doc_structure.cars])
    if doc_structure.list_in_cell:
        if settings.GROUP_CARS:
            car_str = "\n".join(cars)
            row_info.add_car(car_str)
        else:
            for car in cars:
                row_info.add_car(car)
                
    else:
        row_info.add_car(cars)

    
    return row_info.get_entryes()


def xlsx_to_csv(doc_file):

    print(f'Конвертация в csv файла {doc_file.get_file_name()}')
    
    doc_structure = doc_file.get_tab_structure()
    if not doc_structure:
        return False

    Row_Info.set_empty_value_pattern(doc_structure.empty_cell)
    
    
    workbook = xlrd.open_workbook(doc_file.get_file_name(), formatting_info=False)
    #Ищем первый непустой лист
    for sheet in workbook.sheets():
        if sheet.nrows>0:
            ts_sheet = sheet
            break
    else:
        #Нет заполненных листов
        return False

    #У МинСельХоза за 2013 год в одном файле два заполненных листа
    if workbook.sheet_names()==['Лист 1','СВЕДЕНИЯ ЗА 2013 Г.']:
        ts_sheet = workbook.sheet_by_index(1)


    csv_file = open(doc_file.get_csvfile_name(),mode = 'w',newline='')
    csv_writer = csv.DictWriter(csv_file,Row_Info.get_fields(),dialect='excel',delimiter= settings.CSV_DELIMETR)
    #if not csv.Sniffer().has_header(csv_file.read()):
    csv_writer.writeheader()

    caption_list = []
    for str_ind in doc_structure.caption_str:
        row_values = ts_sheet.row_values(str_ind)
        caption_list.append(utils.clear_text_from_noise(" ".join(row_values)))
        #print(f'caption : {caption}')
    
    caption = " ".join(caption_list)

    Row_Info.set_file_info(state_name = doc_file.state_name,
        year = doc_file.year,
        doc_caption = caption,
        file_url = doc_file.doc_url)
    
    list_of_lists = []
    for row_num in range(doc_structure.first_str,ts_sheet.nrows):
        row_values = ts_sheet.row_values(row_num)
        #print('row_values : '+str(row_values))
        if doc_structure.multi_row_value:
            #Если колонка имя заполнена
            if Row_Info.value_not_empty(doc_structure.get_cell('name',row_values)):
                
                for profit_entry in decompose_one_row(list_of_lists,doc_structure):
                    csv_writer.writerow(profit_entry)
                
                list_of_lists = [[value] for value in row_values]

            else:
                list_of_lists = [a+[b] for a,b in zip(list_of_lists, row_values)]

        elif doc_structure.list_in_cell:
            row_values = [str(a).split('\n') for a in row_values]
            for profit_entry in decompose_one_row(row_values,doc_structure):
                    csv_writer.writerow(profit_entry)

        else:

            for profit_entry in decompose_one_row(row_values,doc_structure):
                    csv_writer.writerow(profit_entry)

    csv_file.close()

    return True

def docx_to_csv(doc_file):

    print(f'Конвертация в csv файла {doc_file.get_file_name()}')

    doc_structure = doc_file.get_tab_structure()
    if not doc_structure:
        return False

    Row_Info.set_empty_value_pattern(doc_structure.empty_cell)

    csv_file = open(doc_file.get_csvfile_name(),mode = 'w',newline='')
    csv_writer = csv.DictWriter(csv_file,Row_Info.get_fields(),dialect='excel',delimiter= settings.CSV_DELIMETR)
    csv_writer.writeheader()

    document = zipfile.ZipFile(doc_file.get_file_name())
    xml_content = document.read('word/document.xml')
    document.close()

    soup = BeautifulSoup(xml_content,"html.parser")
    body = soup.find('w:body')


    if len(doc_structure.caption_str )== 0 :
        #Заголовок просто написан сверху
        caption = " ".join(par_str for par_str in 
            ["".join(word.strings) for word in body if word.name == 'w:p']
            if par_str!='')
    else:
        #Заголовок в таблице сверху
        caption = " ".join(par_str for par_str in 
            ["".join(tab.strings) for tab in 
            body.find_all('w:tbl')[doc_structure.caption_str.start:doc_structure.caption_str.stop]]
            if par_str!='')
    

    Row_Info.set_file_info(state_name = doc_file.state_name,
        year = doc_file.year,
        doc_caption = caption,
        file_url = doc_file.doc_url)

    #В некоторых файлах по таблице на лист
    #[caption_str.stop:] исключает заголовочную таблицу
    for tab_count, table in enumerate(body.find_all('w:tbl')[doc_structure.caption_str.stop:],1):
        #Строки
        
        skip_counter = 0
        #В первой таблице всегда есть шапка а в остальных не факт
        first_str = (doc_structure.first_str if tab_count == 1 else 0)
        for tab_row in table.find_all('w:tr')[first_str:]:

            row_values = []
            #Колонки
            for tab_cell in tab_row.find_all('w:tc'):
                #Параграфы (список из параграфов в ячейке)
                row_values.append([ "".join(parag.strings) for parag in tab_cell.find_all('w:p')])

            #print('----------------------------')
            #for num, cell_text in enumerate(row_values):
            #   print(f'{num} : {cell_text}')

            num_pp  = doc_structure.get_cell('num_pp',row_values)
            
            #В некоторых файлах шапка появляется в самых неожиданных местах таблицы
            if num_pp is None:
                pass#штош
            elif skip_counter:
                #print('Пропускаем шапку')
                skip_counter-= 1
                continue
            elif re.search('п/п',str(num_pp)):
                #print('Пропускаем шапку')
                skip_counter = doc_structure.first_str-1
                continue

            
            try:
                row_info = decompose_one_row(row_values,doc_structure)
            except ValueError:
                csv_file.close()
                return False

            for profit_entry in row_info:
                    csv_writer.writerow(profit_entry)

    csv_file.close()
    return True


def convert_file(doc_file):
    
    #Будем форматировать числа в красивый вид
    locale.setlocale(locale.LC_ALL, "")

    Person.restart_clerk_counter()
    Row_Info.restart_error_counter()

    
    if doc_file.its_xlsx():
        file_converted = xlsx_to_csv(doc_file)
    elif doc_file.its_xls():
        file_converted = xlsx_to_csv(doc_file)
    elif doc_file.its_docx():
        file_converted = docx_to_csv(doc_file)
    else:
        print(f'Процедура конвертации для файла с расширением {doc_file.file_extension} не задана')
        return False


    if file_converted:
        print('Файл успешно сконвертирован в csv таблицу')
        print(f'Ошибок при конвертации : {Row_Info.error_counter}')
        return True
    else:
        print('Файл не сконвертирован')
        return False

