# Decision
**De**clarations of **Ci**vil **S**ervants Parser

## Зачем нужен Decision

**Decision** – это сборщик и парсер деклараций о доходах и имуществе государственных служащих, опубликованных на сайтах министерств с 2009 по 2019 год. 

**Decision** разработан командой Центра перспективных управленческих решений. С его помощью мы собрали данные о декларациях, опубликованные в рамках проекта ИНИД (Инфраструктура научно-исследовательских данных). 

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
