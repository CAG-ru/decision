# -*- coding: utf-8 -*-
import re
import requests

from src import doc_converter, settings

def clear_text_from_noise(mb_text):
    if isinstance(mb_text,str):
        #от переносов строки 
        new_text = re.sub(r'(\r\n?|\n)'," ",mb_text)
        #от пустых скобок 
        new_text = re.sub(r'\(\s*\)',"",new_text)
        #от пробелов и запятых в конце и в начале
        new_text = re.sub(r'^\s+|\s+$|,\s*$',"",new_text)
        #от скобок в конце и в начале
        if re.fullmatch(r'^\s*\((\d|\D)*\)\s*$',new_text):
            new_text = re.sub(r'(^\s*\(\s*)|(\s*\)\s*$)',"",new_text)
        #от двойных пробелов 
        new_text = re.sub(r'(\s{2,})'," ",new_text)

        return new_text
    else:
        return mb_text



def download_file(file_properties):
    with requests.Session() as s:
        requests.packages.urllib3.disable_warnings()
        header = {
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'ru,en-US;q=0.7,en;q=0.3',
            'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0',
            #'cache-control':'no-cache',
            #'dnt': '1',
            #'pragma': 'no-cache',
            #'sec-fetch-mode': 'navigate',
            #'sec-fetch-site': 'none',
            #'sec-fetch-user': '?1',
            #'upgrade-insecure-requests': '1',
            }
        for num in range(1,11):

            try:
                web_file = s.get(file_properties.doc_url,headers=header,verify=False,timeout= settings.REQUEST_TIMEOUT)
                break
            except requests.exceptions.RequestException as e:
                print(f'{num}requests {e} error')
        
        else:
            print('10 неудачных попыток скачивания. Файл не загружен.')
            return False

    if web_file.status_code != 200:
        # сообщить об ошибке
        print(f"Скачивание не удалось. Код : {web_file.status_code}")
        print(web_file.content.decode())
        return False

    if web_file.headers['Content-Type'] == 'application/msword':
        file_properties.file_extension = 'doc'
    elif web_file.headers['Content-Type'] == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        file_properties.file_extension = 'docx'
    elif web_file.headers['Content-Type'] == 'application/excel':
        file_properties.file_extension = 'xls'
    elif web_file.headers['Content-Type'] == 'application/vnd.ms-excel':
        file_properties.file_extension = 'xls'
    elif web_file.headers['Content-Type'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        file_properties.file_extension = 'xlsx'
    else:
        print(
            f"Файл с неизвестным расшитением. Content-Type = '{web_file.headers['Content-Type']}'")
        return False

    doc_file = open(file_properties.get_file_name(), "wb")
    doc_file.write(web_file.content)
    doc_file.close()

    if file_properties.its_doc():
        doc_converter.convert_doc_to_docx(file_properties.get_file_name())
        file_properties.file_extension = 'docx'
        
    return True
