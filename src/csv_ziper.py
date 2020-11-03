import os
import sys
import csv
from pathlib import Path

import settings
from doc_parser import Row_Info

def main(files_count):
    csv_filename ='data/declarations.csv'
    open(csv_filename, 'w').close()

    csv_result = open(csv_filename,mode = 'w',newline='')
    csv_writer = csv.DictWriter(csv_result,Row_Info.get_fields(),dialect='excel',delimiter= settings.CSV_DELIMETR)
    csv_writer.writeheader()
    file_paths = sorted(
        (x for x in Path(settings.RESULT_DIR).iterdir() if x.suffix ==".csv")
        ,key=os.path.getmtime)
    for file_path in file_paths[:files_count]:
    
        csv_file = open(file_path,'r')
        csv_reader = csv.DictReader(csv_file,fieldnames=None,dialect='excel',delimiter= settings.CSV_DELIMETR)
        csv_writer.writerows(row for row in csv_reader)
        csv_file.close()

    csv_result.close()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        #значит передано имя обрабатываемого файла
        main(int(sys.argv[1]))
    else:
        main(-1)