# -*- coding: utf-8 -*-
import os
import time

from src import settings

def doc_to_docx_linux(file_name):
    from subprocess import call, PIPE, STDOUT

    try:
        from subprocess import DEVNULL # py3k
    except ImportError:
        DEVNULL = open(os.devnull, 'wb')

    #soffice --headless --convert-to docx --outdir doc_doc doc_doc/mnr_2009.doc

    call([
        'soffice',
        '--headless',
        '--convert-to',
        'docx',
        '--outdir',
        settings.DECLARETION_DIR,
        file_name],
        stdin=PIPE,
        stdout=DEVNULL,
        stderr=STDOUT
        )
    
    now_time = time.time()
    file_name = file_name+"x"#doc->docx
    while not os.path.exists(file_name):
        print('in process...')
        time.sleep(10)
        if time.time()-now_time >60*5:
            raise Exception('doc->docx conversation problem. Timeout expired')
    

def doc_to_docx_win(file_name):
    #Не проверялось
    import win32com.client as win32
    from win32com.client import constants

    # Opening MS Word

    word = win32.gencache.EnsureDispatch('Word.Application')
    doc = word.Documents.Open(file_name)
    doc.Activate ()


     # Save and Close
    word.ActiveDocument.SaveAs(FileFormat=constants.wdFormatXMLDocument)
    doc.Close(False)

def convert_doc_to_docx(file_name):
    print(f'Конвертация в docx формат файла {file_name}')
    if os.name == "posix":
        doc_to_docx_linux(file_name)
    elif os.name == "nt":
        doc_to_docx_win(file_name)

