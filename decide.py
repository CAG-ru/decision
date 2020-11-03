#!/usr/bin/env python3

import argparse
from argparse import RawTextHelpFormatter
import pandas as pd
import os

from src.utils import download_file
from src.doc_parser import convert_file
from src.doc_structures import DocfileProperties

def decide(min_code, min_name, year, config):
    declarations_info = config[(config['Год'] == year) 
            & (config['Код министерства'] == min_code)]

    section_urls = declarations_info['Ссылка на раздел сайта с декларациями'].to_list()
    doc_urls = declarations_info['Ссылка на файл с декларациями'].to_list()

    for s_url, d_url in zip(section_urls, doc_urls):
        declaration_config = DocfileProperties(
                state_abbr=min_code,
                state_name=min_name,
                year=year,
                section_url=s_url,
                doc_url=d_url)

        declaration_downloaded = download_file(declaration_config)

        if declaration_downloaded:
            file_converted = convert_file(declaration_config)           
            
        #else:
            #log warning

def valid_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)
    subdirs = ['csv_files/', 'declaration_files/']
    for sd in subdirs:
        sd_path = os.path.join(path, sd)
        if not os.path.isdir(sd_path):
            os.mkdir(sd_path)

def load_config():
    config = pd.read_csv('config/config.csv', sep=';')
    return config

def available_ministries(config):
    ministries_info = config.filter(items=
            ['Код министерства', 'Наименование министерства'])
    ministries_info.drop_duplicates(subset='Код министерства', inplace=True)
    ministries_info.set_index('Код министерства', drop=True, inplace=True)
    ministries = ministries_info.to_dict()['Наименование министерства']
    return ministries

def available_years(config):
    years = set(config['Год'].astype(str).to_list())
    return years

def years_range(years_list):
    int_years = [int(year) for year in years_list]
    return str(min(int_years)), str(max(int_years))

def parse_args(config):
    parser = argparse.ArgumentParser(
        description='''Парсинг деклараций доходов 
        и имущества в разделе министерств и лет''',
        add_help=True,
        formatter_class=RawTextHelpFormatter)

    # Министерство
    ministries = available_ministries(config)
    ministry_help = 'Код министерства, опубликовавшего декларацию\n' + '\n'.join(
            '{} : {}'.format(key, value)
            for key, value in ministries.items())
    parser.add_argument('-m', '--ministry', 
            choices=ministries, help=ministry_help, metavar='', required=True)

    # Год
    years = available_years(config)
    min_year, max_year = years_range(years)
    year_help = 'Год опубликования декларации с {} по {}'.format(min_year, max_year) 
    parser.add_argument('-y', '--year', choices=years, 
            help=year_help, metavar='', required=True)

    # Рабочая директория
    parser.add_argument('-w', '--workdir', type=valid_dir, required=True,
            help='Рабочая директория', metavar='')

    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')

    args = parser.parse_args()

    args.ministry_name = ministries[args.ministry]
    
    return args

if __name__ == '__main__':
    config = load_config()
    args = parse_args(config)
    decide(args.ministry, args.ministry_name, int(args.year), config)
