# Decision
**De**clarations of **Ci**vil **S**ervants Parser

## Зачем нужен Decision

**Decision** – это сборщик и парсер деклараций о доходах и имуществе государственных служащих, опубликованных на сайтах министерств с 2009 по 2019 год. 

**Decision** разработан командой Центра перспективных управленческих решений. С его помощью мы собрали данные о декларациях, [опубликованные](https://data-in.ru/data-catalog/datasets/150/) в рамках проекта ИНИД (Инфраструктура научно-исследовательских данных). 

## Быстрый старт

Чтобы скачать и распарсить все поданные МВД в 2016 году декларации о доходах и сохранить результаты в `data`, достаточно запустить `decide.py`:

```shell
python decide.py -m mvd -y 2016 -w data
```
## Установка

*Внимание: пока полностью поддерживается только Linux и MacOS!*

Рекомендации по установки с помощью `pip`.

### Linux

```shell
apt-get install soffice
git clone git@github.com:CAG-ru/decision.git
pip install requirements.txt
```
### MacOS

```shell
brew install libreoffice
git clone git@github.com:CAG-ru/decision.git
pip install requirements.txt
```
## Использование

Чтобы собрать данные по одному году и министерству, можно воспользоваться скриптом `decide.py`:

```
python decide.py --help
usage: decide.py [-h] -m  -y  -w  [-v]

Парсинг деклараций доходов
        и имущества в разделе министерств и лет

optional arguments:
  -h, --help        show this help message and exit
  -m , --ministry   Код министерства, опубликовавшего декларацию
                    minzdrav : Министерство здравоохранения РФ
                    mvd : Министерство внутренних дел РФ
                    mid : Министерство иностранных дел РФ
                    minjust : Министерство юстиции РФ
                    mincult : Министерство культуры РФ
                    minobr : Министерство науки и высшего образования РФ
                    mnr : Министерство природных ресурсов и экологии РФ
                    minprom : Министерство промышленности и торговли РФ
                    edu : Министерство просвещения РФ
                    minvr : Министерство Российской Федерации по развитию Дальнего Востока и Арктики (Минвостокразвития России)
                    mcx : Министерство сельского хозяйства РФ
                    minsport : Министерство спорта РФ
                    minstroy : Министерство строительства и жилищно-коммунального хозяйства РФ
                    mintrans : Министерство транспорта РФ
                    mintrud : Министерство труда и социальной защиты РФ
                    minfin : Министерство финансов РФ
                    digital : Министерство цифрового развития, связи и массовых коммуникаций Российской Федерации
                    economy : Министерство экономического развития РФ
                    minenergo : Министерство энергетики РФ
  -y , --year       Год опубликования декларации с 2009 по 2019
  -w , --workdir    Рабочая директория
  -v, --version     show program's version number and exit
```

Данные о декларациях (включая полное наименование министерства, `url` скачиваемых документов, а также ссылки на разделы сайтов министерств, где хранятся декларации) находятся в конфигурационном файле `config/config.csv`. 

Мы скоро добавим возможность для пользователей дополнять конфигурационные файлы парсера, чтобы его можно было использовать для других, нестандартных деклараций.

Пример того, как парсер используется сразу для всех деклараций, можно посмотреть в `jupyter notebook` `generate_income_data.ipynb`. В этом ноутбуке можно воспроизвести постпроцессинг данных, в результате которого мы получили опубликованный датасет с доходами чиновников.

## Контакты

Ольга Батова, [o.batova@cpur.ru]
Витовт Копыток, [v.kopytok@cpur.ru]
