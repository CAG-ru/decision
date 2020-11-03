# -*- coding: utf-8 -*-

import xlrd
import os
import sys

import settings
import utils
import doc_parser
from doc_structures import DocfileProperties

def main(start_num = None,end_num = None):
    if start_num == None:
        check_range = False
        num_range = range(0)
    else:
        check_range = True
        num_range = range(int(start_num),int(end_num)+1)

    if not os.path.exists(settings.DECLARETION_DIR):
        os.mkdir(settings.DECLARETION_DIR)

    if not os.path.exists(settings.RESULT_DIR):
        os.mkdir(settings.RESULT_DIR)

    workbook = xlrd.open_workbook(
        settings.REGISTRY_FILE, formatting_info=False)
    sheet = workbook.sheet_by_name('reestr')
    #Прочитаем заголовки
    cell_match = {}
    row_values = sheet.row_values(1)
    for cell_num, cell_str in enumerate(row_values):
        cell_match[cell_str] = cell_num

    #Заголовки:
    #file_name - как называть полученые файлы, оно же имя словаря
        #загружаем только те что с заполненым именем
    #statebody - формальное название министерства. тоже надо грузить
    #section_name
    #section_url - ссылка на раздел с файлами
    #year - год
    #declaration_name
    #declaration_url - ссылка откуда качали (надо вставить в csv)
    #format
    #clerks
    #minister
    #other
    #mark
    #comment
    #parsing - да/нет нужно ли разбирать

    for row_num in range(2,sheet.nrows):
        row_values = sheet.row_values(row_num)
        state_abbr = row_values[cell_match.get('file_name')]
        state_name = row_values[cell_match.get('statebody')]
        parsing = row_values[cell_match.get('parsing')]
        
        if not state_abbr or parsing != 'yes':
            continue
        elif check_range and row_num+1 not in num_range:
            continue
        
        year = row_values[cell_match.get('year')]
        section_url = row_values[cell_match.get('section_url')]

if __name__ == '__main__':
    args = parse_args()
        doc_url = row_values[cell_match.get('declaration_url')]
        doc_file = DocfileProperties(
            state_abbr = state_abbr,
            state_name = state_name,
            year = year,
            section_url = section_url,
            doc_url = doc_url)

        file_downloaded = utils.download_file(doc_file)

        if not file_downloaded:
            continue

        file_converted = doc_parser.convert_file(doc_file)
