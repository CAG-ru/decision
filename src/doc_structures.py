# -*- coding: utf-8 -*-

from src import settings

#Свойства файла разбираемого документа
class DocfileProperties():
    same_year_count = 0
    same_year_value = ""
    
    def __init__(self,
        state_abbr = "",
        state_name = "",
        year = "",
        section_url = "",
        doc_url = ""):
        
        self.directory = settings.DECLARETION_DIR
        self.file_extension = ""
        self.state_abbr = state_abbr
        self.state_name = state_name
        self.year = str(int(year))#там float! 2019.0
        self.section_url = section_url
        self.doc_url = doc_url

        if self.year == DocfileProperties.same_year_value:
            DocfileProperties.same_year_count+=1
        else:
            DocfileProperties.same_year_value = self.year
            DocfileProperties.same_year_count = 0



    def get_file_name(self,file_extension = ""):
        file_name = (
            self.directory 
            + "/" 
            + self.state_abbr 
            + "_" 
            + self.year 
            +(f"({DocfileProperties.same_year_count})" if DocfileProperties.same_year_count>0 else "")
            + "."
            +self.file_extension)

        return file_name

    def get_csvfile_name(self):
        file_name = (
            settings.RESULT_DIR 
            + "/" 
            + self.state_abbr 
            + "_" 
            + self.year 
            +(f"({DocfileProperties.same_year_count})" if DocfileProperties.same_year_count>0 else "")
            + ".csv")
        return file_name
    

    def its_doc(self):
        return (self.file_extension == "doc")

    def its_xls(self):
        return (self.file_extension == "xls")

    def its_xlsx(self):
        return (self.file_extension == "xlsx")

    def its_docx(self):
        return (self.file_extension == "docx")


    def get_tab_structure(self):
        new_matching = cell_matching()

        if (
            self.state_abbr == 'minzdrav' 
            and self.year in ['2019','2018','2017']
            ):
            new_matching.first_str = 3
            new_matching.empty_cell = "-"
        
        elif (
            self.state_abbr == 'minzdrav' 
            and self.year in ['2016','2015']
            and DocfileProperties.same_year_count == 0
            ):
            new_matching.first_str = 2
            new_matching.empty_cell = "-"
        
        elif (
            self.state_abbr == 'minzdrav' 
            and self.year in ['2016',] 
            and DocfileProperties.same_year_count == 1
            ):
            new_matching.first_str = 2
            new_matching.empty_cell = "-"
            new_matching.cells_count = 12
            
            new_matching.num_pp = None
            new_matching.name = 0
            new_matching.position = 1
            new_matching.ownflats_type = 2
            new_matching.ownflats_owntype = 3
            new_matching.ownflats_meters = 4
            new_matching.ownflats_country = 5
            new_matching.rentflats_type = 6
            new_matching.rentflats_meters = 7
            new_matching.rentflats_country = 8
            new_matching.cars = 9
            new_matching.money = 10
            new_matching.source = 11
        elif (
            self.state_abbr == 'minzdrav' 
            and self.year in ['2014',] 
            ):
            new_matching.first_str = 2
            new_matching.empty_cell = "-"
            new_matching.cells_count = 12
            new_matching.list_in_cell = True
            
            new_matching.num_pp = None
            new_matching.name = 0
            new_matching.position = 1
            new_matching.ownflats_type = 2
            new_matching.ownflats_owntype = 3
            new_matching.ownflats_meters = 4
            new_matching.ownflats_country = 5
            new_matching.rentflats_type = 6
            new_matching.rentflats_meters = 7
            new_matching.rentflats_country = 8
            new_matching.cars = 9
            new_matching.money = 10
            new_matching.source = 11
        # minzdrav 2013, 2012 
        elif (
            self.state_abbr == 'minzdrav' 
            and self.year in ['2013','2012']
            and DocfileProperties.same_year_count == 0
            ):
            new_matching.first_str = 2
            new_matching.empty_cell = ""
        # mvd 2019 
        elif (
            self.state_abbr == 'mvd' 
            and self.year in ['2019',]
            ):
            new_matching.first_str = 17
            new_matching.empty_cell = r"(не имеет)|-"
            new_matching.cells_count = 19 
            new_matching.caption_str = range(1,2)

            new_matching.num_pp = 1#B
            new_matching.name = 2#C
            new_matching.position = 3#D
            new_matching.ownflats_type = 4#E
            new_matching.ownflats_owntype = 5#F
            new_matching.ownflats_meters = 6#G
            new_matching.ownflats_country = 7#H
            new_matching.rentflats_type = 8#I
            new_matching.rentflats_meters = 9#J
            new_matching.rentflats_country = 10#K
            new_matching.cars = 11#L
            new_matching.money = 12#M
            new_matching.source = 13#N
        
        # mvd 2018, 2017 
        elif (
            self.state_abbr == 'mvd' 
            and self.year in ['2018','2017']
            ):
            new_matching.first_str = 17
            new_matching.empty_cell = r"(не имеет)|-"
            new_matching.cells_count = 14 
            new_matching.caption_str = range(1,2)

            new_matching.num_pp = 1#B
            new_matching.name = 2#C
            new_matching.position = 3#D
            new_matching.ownflats_type = 4#E
            new_matching.ownflats_owntype = 5#F
            new_matching.ownflats_meters = 6#G
            new_matching.ownflats_country = 7#H
            new_matching.rentflats_type = 8#I
            new_matching.rentflats_meters = 9#J
            new_matching.rentflats_country = 10#K
            new_matching.cars = 11#L
            new_matching.money = 12#M
            new_matching.source = 13#N
        
        # mvd 2016 
        elif (
            self.state_abbr == 'mvd' 
            and self.year in ['2016',]
            ):
            new_matching.first_str = 11
            new_matching.empty_cell = r"(не имеет)|-"
            new_matching.cells_count = 13 
            new_matching.caption_str = range(1,2)

            new_matching.num_pp = 0#A
            new_matching.name = 1#B
            new_matching.position = 2#C
            new_matching.ownflats_type = 4#E
            new_matching.ownflats_owntype = 5#F
            new_matching.ownflats_meters = 6#G
            new_matching.ownflats_country = 7#H
            new_matching.rentflats_type = 8#I
            new_matching.rentflats_meters = 9#J
            new_matching.rentflats_country = 10#K
            new_matching.cars = 11#L
            new_matching.money = 3#D
            new_matching.source = 12#M
        
        # mvd 2015, 2014 
        elif (
            self.state_abbr == 'mvd' 
            and self.year in ['2015','2014']
            ):
            new_matching.first_str = 16
            new_matching.empty_cell = r"(не имеет)|-"
            new_matching.cells_count = 14
            new_matching.caption_str = range(1,2)

            new_matching.num_pp = 1#B
            new_matching.name = 2#C
            new_matching.position = 3#D
            new_matching.ownflats_type = 5#F
            new_matching.ownflats_owntype = 6#G
            new_matching.ownflats_meters = 7#H
            new_matching.ownflats_country = 8#I
            new_matching.rentflats_type = 9#J
            new_matching.rentflats_meters = 10#K
            new_matching.rentflats_country = 11#L
            new_matching.cars = 12#M
            new_matching.money = 4#E
            new_matching.source = 13#N
        
        # mvd 2013 
        elif (
            self.state_abbr == 'mvd' 
            and self.year in ['2013',]
            ):
            new_matching.first_str = 12
            new_matching.empty_cell = r"(не имеет)|-"
            new_matching.cells_count = 13
            new_matching.caption_str = range(0,2)
            new_matching.multi_row_value = True

            new_matching.num_pp = 0#A
            new_matching.name = 1#B
            new_matching.position = 2#C
            new_matching.ownflats_type = 4#E
            new_matching.ownflats_owntype = 5#F
            new_matching.ownflats_meters = 6#G
            new_matching.ownflats_country = 7#H
            new_matching.rentflats_type = 8#I
            new_matching.rentflats_meters = 9#J
            new_matching.rentflats_country = 10#K
            new_matching.cars = 11#L
            new_matching.money = 3#D
            new_matching.source = 12#M
        
        # mid 2019, 2018, 2016, 2015, 2014,2013
        elif (
            self.state_abbr == 'mid' 
            and self.year in ['2019','2018','2016','2015','2014','2013']
            ):
            new_matching.first_str = 2
            new_matching.empty_cell = ""
            new_matching.list_in_cell = True

        # minjust 2019,2018,2016
        elif (
            self.state_abbr == 'minjust' 
            and self.year in ['2019','2018','2016']
            ):
            new_matching.first_str = 2
            new_matching.empty_cell = r"–\-"
            new_matching.list_in_cell = True
            new_matching.split_cells =[5,]
            new_matching.cells_count = 13
            new_matching.extra_cells_intheend = range(0,4)

        # mincult 2019
        elif (
            self.state_abbr == 'mincult' 
            and self.year in ['2019',]
            ):
            new_matching.empty_cell = "-"
            new_matching.cells_count = 13

            new_matching.num_pp = None

        # mincult 2018, 2017, 2016, 2015, 2014, 2013
        elif (
            self.state_abbr == 'mincult' 
            and self.year in ['2018','2017','2016','2015','2014','2013']
            ):
            new_matching.first_str = 2
            new_matching.empty_cell = "-"
            new_matching.cells_count = 13

            new_matching.num_pp = None#В одной строке забыли про номер

        # minobr 2019
        elif (
            self.state_abbr == 'minobr' 
            and self.year in ['2019',]
            ):
            new_matching.first_str = 3
            new_matching.caption_str = range(0)
            new_matching.empty_cell = r"\-(нет)"
            new_matching.cells_count = 13

        # minobr 2018
        elif (
            self.state_abbr == 'minobr' 
            and self.year in ['2018']
            ):
            new_matching.first_str = 3
            new_matching.caption_str = range(0)
            new_matching.empty_cell = r"\-(нет)"
            new_matching.cells_count = 13

            new_matching.num_pp = None#У Герцена неправильное форматирование

        # minr 2019, 2016, 2014, 2013
        elif (
            self.state_abbr == 'mnr' 
            and self.year in ['2019','2016','2014','2013']
            ):
            new_matching.first_str = 2
            new_matching.cells_count = 13
            new_matching.list_in_cell = True
            new_matching.empty_cell = r"\-"
        
        # minr 2018, 2017, 2015
        elif (
            self.state_abbr == 'mnr' 
            and self.year in ['2018','2017','2015']
            ):
            new_matching.first_str = 2
            new_matching.cells_count = 13
            new_matching.list_in_cell = True
            new_matching.empty_cell = r"\-"
            new_matching.num_pp = None#В одной строке забыли про номер
        
        # minprom 2019,2018,2017
        elif (
            self.state_abbr == 'minprom' 
            and self.year in ['2019','2018','2017']
            ):
            new_matching.first_str = 2
            new_matching.empty_cell = "-"
            new_matching.cells_count = 13

            new_matching.num_pp = None#В одной строке забыли про номер

        # minprom 2016 (0)
        elif (
            self.state_abbr == 'minprom' 
            and self.year in ['2019','2018','2017','2016']
            and DocfileProperties.same_year_count == 0
            ):
            new_matching.first_str = 2
            new_matching.empty_cell = "-"
            new_matching.cells_count = 13

            new_matching.num_pp = None#В одной строке забыли про номер

        # minprom 2016 (1)
        elif (
            self.state_abbr == 'minprom' 
            and self.year in ['2019','2018','2017','2016']
            and DocfileProperties.same_year_count == 1
            ):
            new_matching.first_str = 3
            new_matching.empty_cell = "-"
            new_matching.cells_count = 13

            new_matching.num_pp = None#В одной строке забыли про номер

        # minprom 2015
        elif (
            self.state_abbr == 'minprom' 
            and self.year in ['2015',] 
            ):
            new_matching.first_str = 2
            new_matching.empty_cell = "-"
            new_matching.cells_count = 12
            
            new_matching.num_pp = None
            new_matching.name = 0
            new_matching.position = 1
            new_matching.ownflats_type = 2
            new_matching.ownflats_owntype = 3
            new_matching.ownflats_meters = 4
            new_matching.ownflats_country = 5
            new_matching.rentflats_type = 6
            new_matching.rentflats_meters = 7
            new_matching.rentflats_country = 8
            new_matching.cars = 9
            new_matching.money = 10
            new_matching.source = 11

        # minprom 2014
        elif (
            self.state_abbr == 'minprom' 
            and self.year in ['2014',] 
            ):
            new_matching.first_str = 3
            new_matching.empty_cell = "-"
            new_matching.cells_count = 13
            
            new_matching.num_pp = None
            new_matching.name = 0
            
            new_matching.family = 1
            new_matching.insert_cells_ind = 3
        
        # edu 2019
        elif (
            self.state_abbr == 'edu' 
            and self.year in ['2019',] 
            ):
            new_matching.first_str = 3
            new_matching.empty_cell = "-"
            
        # minvr 2019
        elif (
            self.state_abbr == 'minvr' 
            and self.year in ['2019',] 
            ):
            new_matching.first_str = 3
            new_matching.empty_cell = "-"
        
            new_matching.num_pp = None#Номера у жен и детей
            
        # minvr 2018,2017,2016,2015,2014
        elif (
            self.state_abbr == 'minvr' 
            and self.year in ['2018','2017','2016','2015','2014']
            ):
            new_matching.first_str = 4
            new_matching.empty_cell = r"\-"
            new_matching.extra_cells_intheend = range(0,6)
        
        # minvr 2013
        elif (
            self.state_abbr == 'minvr' 
            and self.year in ['2013',]
            ):
            new_matching.first_str = 5
            new_matching.empty_cell = r"\-"
            new_matching.caption_str = range(0,3)
            
            new_matching.num_pp = None#Номера у жены Грачева

        # mcx 2019
        elif (
            self.state_abbr == 'mcx' 
            and self.year in ['2019',]
            ):
            new_matching.empty_cell = r"\-"
            new_matching.first_str = 5
            new_matching.caption_str = range(0, 3)

        # mcx 2017(0)
        elif (
            self.state_abbr == 'mcx' 
            and self.year in ['2017',]
            and DocfileProperties.same_year_count == 0
            ):
            new_matching.empty_cell = r"\-"
            new_matching.first_str = 5
            new_matching.caption_str = range(0, 3)

            new_matching.num_pp = None#пропущен номер у чиновника

        # mcx 2016(5,7)
        elif (
            self.state_abbr == 'mcx' 
            and self.year in ['2016',]
            and DocfileProperties.same_year_count in [5,7]
            ):
            new_matching.empty_cell = r"\-"
            new_matching.first_str = 5
            new_matching.caption_str = range(0, 3)

            new_matching.num_pp = None#пропущен номер у чиновника

        # mcx 2014(13),2013(13)
        elif (
            self.state_abbr == 'mcx' 
            and self.year in ['2014','2013']
            and DocfileProperties.same_year_count in [13,]
            ):
            new_matching.empty_cell = r"\-"
            new_matching.first_str = 5
            new_matching.caption_str = range(0, 3)

            new_matching.num_pp = None#пропущен номер у чиновника

        # mcx 2018,2017,2016,2015,2014,2013
        elif (
            self.state_abbr == 'mcx' 
            and self.year in ['2018','2017','2016','2015','2014','2013']
            ):
            new_matching.empty_cell = r"_\-"
            new_matching.first_str = 5
            new_matching.caption_str = range(0, 3)

        # mcx 2012(3)
        elif (
            self.state_abbr == 'mcx' 
            and self.year in ['2012',]
            and DocfileProperties.same_year_count in [3,]
            ):
            new_matching.empty_cell = r"_\-"
            new_matching.first_str = 5
            new_matching.caption_str = range(0, 3)
            new_matching.cells_count = 13

            new_matching.transform_function = new_matching.transform_mcx2012

            new_matching.num_pp = None #A(None если нет)
            new_matching.name = 0#A
            new_matching.position = 1#B
            new_matching.ownflats_type = 2#C
            #В колонке 3 мусор
            new_matching.ownflats_owntype = 11#добавляется постобработкой
            new_matching.ownflats_meters = 4#E
            new_matching.ownflats_country = 5#F
            new_matching.rentflats_type = 7#H
            new_matching.rentflats_meters = 8#I
            new_matching.rentflats_country = 9#J
            new_matching.cars = 6#G
            new_matching.money = 10#K
            new_matching.source = 12#добавляется постобработкой

        # mcx 2012(7,11,13)
        elif (
            self.state_abbr == 'mcx' 
            and self.year in ['2012',]
            and DocfileProperties.same_year_count in [7,11,13]
            ):
            new_matching.empty_cell = r"_\-"
            new_matching.first_str = 5
            new_matching.caption_str = range(0, 3)
            new_matching.cells_count = 13

            new_matching.transform_function = new_matching.transform_mcx2012
            #Колонка А скрыта
            new_matching.num_pp = None #A(None если нет)
            new_matching.name = 1#B
            new_matching.position = 2#C
            new_matching.ownflats_type = 3#D
            new_matching.ownflats_owntype = 11#добавляется постобработкой
            new_matching.ownflats_meters = 4#E
            new_matching.ownflats_country = 5#F
            new_matching.rentflats_type = 7#H
            new_matching.rentflats_meters = 8#I
            new_matching.rentflats_country = 9#J
            new_matching.cars = 6#G
            new_matching.money = 10#K
            new_matching.source = 12#добавляется постобработкой

        # mcx 2012
        elif (
            self.state_abbr == 'mcx' 
            and self.year in ['2012',]
            ):
            new_matching.empty_cell = r"_\-"
            new_matching.first_str = 5
            new_matching.caption_str = range(0, 3)
            new_matching.cells_count = 12

            new_matching.transform_function = new_matching.transform_mcx2012

            new_matching.num_pp = None #A(None если нет)
            new_matching.name = 0#A
            new_matching.position = 1#B
            new_matching.ownflats_type = 2#C
            new_matching.ownflats_owntype = 10#добавляется постобработкой
            new_matching.ownflats_meters = 3#D
            new_matching.ownflats_country = 4#E
            new_matching.rentflats_type = 6#G
            new_matching.rentflats_meters = 7#H
            new_matching.rentflats_country = 8#I
            new_matching.cars = 5#F
            new_matching.money = 9#J
            new_matching.source = 11#добавляется постобработкой

        # minsport 2019,2018
        elif (
            self.state_abbr == 'minsport' 
            and self.year in ['2019','2018']
            ):
            new_matching.empty_cell = r"\-"

        # minsport 2017,2016
        elif (
            self.state_abbr == 'minsport' 
            and self.year in ['2017','2016']
            ):
            new_matching.empty_cell = r"\-"
            new_matching.num_pp = None#Номера у жен и детей
            new_matching.extra_cells_intheend = range(0,4)
        
        # minsport 2015
        elif (
            self.state_abbr == 'minsport' 
            and self.year in ['2015',]
            ):
            new_matching.empty_cell = r"\-"
            new_matching.first_str = 2

        # minsport 2014,2013
        elif (
            self.state_abbr == 'minsport' 
            and self.year in ['2014','2013']
            ):
            new_matching.empty_cell = r"\-"
            new_matching.num_pp = None#Нумератор
            new_matching.first_str = 3

        # minstroy 2019,2018,2017,2016,2015
        elif (
            self.state_abbr == 'minstroy' 
            and self.year in ['2019','2018','2017','2016','2015']
            ):
            new_matching.caption_str = range(3,8)
            new_matching.first_str = 11
            new_matching.cells_count = 139
            new_matching.empty_cell = r"\-_"
            new_matching.extra_cells_intheend = range(0,17)
            
            
            new_matching.num_pp = 0
            new_matching.name = [5,6]
            new_matching.family = None
            new_matching.position = [26,27]
            new_matching.ownflats_type = 47
            new_matching.ownflats_owntype = 58
            new_matching.ownflats_meters = 68
            new_matching.ownflats_country = 76
            new_matching.rentflats_type = 87
            new_matching.rentflats_meters = 98
            new_matching.rentflats_country = 106
            new_matching.cars = 117
            new_matching.money = 128
            new_matching.source = 138

        # minstroy 2014
        elif (
            self.state_abbr == 'minstroy' 
            and self.year in ['2014',]
            ):
            new_matching.first_str = 2
            new_matching.cells_count = 13
            new_matching.extra_cells_intheend = range(0,2)
            new_matching.empty_cell = r"\-"
            
        # minstroy 2013
        elif (
            self.state_abbr == 'minstroy' 
            and self.year in ['2013',]
            ):
            new_matching.first_str = 2
            new_matching.cells_count = 12
            new_matching.extra_cells_intheend = range(0,2)
            new_matching.empty_cell = r"\-"

            new_matching.num_pp = 3
            new_matching.name = 0
            new_matching.position = 1
            new_matching.money = 2
            #transform_minstroy2012 заполняет первые 4 колонки остальное оставляет пустым
            new_matching.ownflats_type = 4
            new_matching.ownflats_owntype = 4
            new_matching.ownflats_meters = 4
            new_matching.ownflats_country = 4
            new_matching.rentflats_type = 4
            new_matching.rentflats_meters = 4
            new_matching.rentflats_country = 4
            new_matching.cars = 4
            new_matching.source = 4

            new_matching.transform_function = new_matching.transform_minstroy2013
            
        # mintrans 2019
        elif (
            self.state_abbr == 'mintrans' 
            and self.year in ['2019',]
            ):
            new_matching.first_str = 4
            new_matching.empty_cell = r"\-"

        # mintrans 2018,2017
        elif (
            self.state_abbr == 'mintrans' 
            and self.year in ['2018','2017']
            ):
            new_matching.first_str = 4
            new_matching.empty_cell = r"\-"
            new_matching.transform_function = new_matching.transform_mintrans2018

            new_matching.num_pp = None

        # mintrans 2016(0),2015(0),2014(0),2013(0)
        elif (
            self.state_abbr == 'mintrans' 
            and self.year in ['2016','2015','2014','2013']
            and DocfileProperties.same_year_count == 0
            ):
            new_matching.first_str = 2
            new_matching.empty_cell = r"\-"
            new_matching.transform_function = new_matching.transform_mintrans2018

            new_matching.num_pp = None
        
        # mintrans 2016(1),2015(1),2014(1),2013(1)
        elif (
            self.state_abbr == 'mintrans' 
            and self.year in ['2016','2015','2014','2013']
            and DocfileProperties.same_year_count == 1
            ):
            new_matching.first_str = 4
            new_matching.empty_cell = r"\-"
            new_matching.transform_function = new_matching.transform_mintrans2018

            new_matching.num_pp = None
        
        # mintrud 2019,2018,2017,2016,2015,2014,2013
        elif (
            self.state_abbr == 'mintrud' 
            and self.year in ['2019','2018','2017','2016','2015','2014','2013']
            ):
            new_matching.first_str = 2
            new_matching.empty_cell = r"\-"

        # minfin 2019
        elif (
            self.state_abbr == 'minfin' 
            and self.year in ['2019',]
            ):
            new_matching.first_str = 9
            new_matching.caption_str = range(1,3)
            
        # minfin 2018, 2014,2013
        elif (
            self.state_abbr == 'minfin' 
            and self.year in ['2018','2014','2013']
            ):
            new_matching.first_str = 11
            
        # minfin 2017
        elif (
            self.state_abbr == 'minfin' 
            and self.year in ['2017',]
            ):
            new_matching.first_str = 10
            new_matching.caption_str = range(0,2)
            
        # minfin 2016
        elif (
            self.state_abbr == 'minfin' 
            and self.year in ['2016',]
            ):
            new_matching.first_str = 12
            new_matching.caption_str = range(0,4)
            new_matching.list_in_cell = True
            
        # minfin 2015
        elif (
            self.state_abbr == 'minfin' 
            and self.year in ['2015',]
            ):
            new_matching.first_str = 9
            new_matching.caption_str = range(0,2)
            
        # digital 2019, 2018
        elif (
            self.state_abbr == 'digital' 
            and self.year in ['2019','2018']
            ):
            new_matching.first_str = 3
            new_matching.caption_str = range(0,2)
        
        # digital 2017
        elif (
            self.state_abbr == 'digital' 
            and self.year in ['2017',]
            ):
            new_matching.first_str = 3
            new_matching.cells_count = 12
            
            new_matching.num_pp = None
            new_matching.name = 0
            new_matching.position = 1
            new_matching.ownflats_type = 2
            new_matching.ownflats_owntype = 3
            new_matching.ownflats_meters = 4
            new_matching.ownflats_country = 5
            new_matching.rentflats_type = 6
            new_matching.rentflats_meters = 7
            new_matching.rentflats_country = 8
            new_matching.cars = 9
            new_matching.money = 10
            new_matching.source = 11
            
        # digital 2016
        elif (
            self.state_abbr == 'digital' 
            and self.year in ['2016',]
            ):
            new_matching.caption_str = range(0,2)
            new_matching.first_str = 6
            new_matching.cells_count = 139
            new_matching.empty_cell = r"\-(не имеет)"
            
            
            new_matching.num_pp = 0
            new_matching.name = 5
            new_matching.family = 6
            new_matching.position = 27
            new_matching.ownflats_type = 47
            new_matching.ownflats_owntype = 58
            new_matching.ownflats_meters = 68
            new_matching.ownflats_country = 76
            new_matching.rentflats_type = 87
            new_matching.rentflats_meters = 98
            new_matching.rentflats_country = 106
            new_matching.cars = 117
            new_matching.money = 128
            new_matching.source = 138
            
        # digital 2015,2014,2013
        elif (
            self.state_abbr == 'digital' 
            and self.year in ['2015','2014','2013']
            ):
            new_matching.caption_str = range(5,8)
            new_matching.first_str = 11
            new_matching.cells_count = 139
            new_matching.empty_cell = r"\-(не имеет)"
            
            
            new_matching.num_pp = 0
            new_matching.name = 5
            new_matching.family = 6
            new_matching.position = 27
            new_matching.ownflats_type = 47
            new_matching.ownflats_owntype = 58
            new_matching.ownflats_meters = 68
            new_matching.ownflats_country = 76
            new_matching.rentflats_type = 87
            new_matching.rentflats_meters = 98
            new_matching.rentflats_country = 106
            new_matching.cars = 117
            new_matching.money = 128
            new_matching.source = 138
            
        # economy 2019
        elif (
            self.state_abbr == 'economy' 
            and self.year in ['2019',]
            ):
            new_matching.first_str = 3
            new_matching.empty_cell = "-"
            new_matching.caption_str = range(0,1)
            new_matching.extra_cells_intheend = range(0,4)

            new_matching.num_pp = None#там нумератор
        
        # economy 2018,2017
        elif (
            self.state_abbr == 'economy' 
            and self.year in ['2018','2017']
            ):
            new_matching.first_str = 0
            new_matching.empty_cell = r"\-"
            
            new_matching.num_pp = None#там нумератор
        
        # economy 2016,2015
        elif (
            self.state_abbr == 'economy' 
            and self.year in ['2016','2015']
            ):
            new_matching.first_str = 0
            new_matching.empty_cell = r"\-"
            new_matching.cells_count = 14
            
            new_matching.num_pp = 0
            new_matching.name = 1
            new_matching.family = 2
            new_matching.position = 3
            new_matching.ownflats_type = 4
            new_matching.ownflats_owntype = 5
            new_matching.ownflats_meters = 6
            new_matching.ownflats_country = 7
            new_matching.rentflats_type = 8
            new_matching.rentflats_meters = 9
            new_matching.rentflats_country = 10
            new_matching.cars = 11
            new_matching.money = 12
            new_matching.source = 13
            
        # economy 2014
        elif (
            self.state_abbr == 'economy' 
            and self.year in ['2014',]
            ):
            new_matching.caption_str = range(0,1)
            new_matching.first_str = 2
            new_matching.empty_cell = r"\-"
                        
            new_matching.transform_function = new_matching.transform_row_1
            
        # economy 2013
        elif (
            self.state_abbr == 'economy' 
            and self.year in ['2013',]
            ):
            new_matching.first_str = 3
            new_matching.empty_cell = r"\-"
            new_matching.num_pp = None
                        
            new_matching.transform_function = new_matching.transform_row_2
            
        
        # minenergo 2019,2018,2017,2016,2015,2013,2010
        elif (
            self.state_abbr == 'minenergo' 
            and self.year in ['2019','2018','2017','2016','2015','2013','2010']
            ):
            new_matching.first_str = 2
            new_matching.empty_cell = r"\-"
            
        # minenergo 2012,2009
        elif (
            self.state_abbr == 'minenergo' 
            and self.year in ['2012','2009']
            ):
            new_matching.first_str = 2
            new_matching.empty_cell = r"\-"
            new_matching.num_pp = None#там нумератор
            
        # minenergo 2014(0)
        elif (
            self.state_abbr == 'minenergo' 
            and self.year in ['2014',]
            and DocfileProperties.same_year_count == 0
            ):
            new_matching.first_str = 2
            new_matching.empty_cell = r""
            new_matching.cells_count = 12
            new_matching.transform_function = new_matching.transform_minenergo2014
            
            new_matching.num_pp = None
            new_matching.name = 0
            new_matching.family = None
            new_matching.position = 1
            new_matching.ownflats_type = 3
            new_matching.ownflats_owntype = 4
            new_matching.ownflats_meters = 5
            new_matching.ownflats_country = 6
            new_matching.rentflats_type = 7
            new_matching.rentflats_meters = 8
            new_matching.rentflats_country = 9
            new_matching.cars = 10
            new_matching.money = 2
            new_matching.source = 11
        
        # minenergo 2014(1)
        elif (
            self.state_abbr == 'minenergo' 
            and self.year in ['2014',]
            and DocfileProperties.same_year_count == 1
            ):
            new_matching.first_str = 2
            new_matching.empty_cell = r"\-"
            new_matching.num_pp = None#там нумератор
            
        
        # minenergo 2011
        elif (
            self.state_abbr == 'minenergo' 
            and self.year in ['2011',]
            ):
            new_matching.first_str = 2
            new_matching.empty_cell = r"\-"
            new_matching.insert_cells_ind = 12
            new_matching.num_pp = None#номер у жены Королева
        else:
            print(f'Не заданы настройки загрузки для {self.state_abbr} {self.year} года')
            return None

        return new_matching


#объекты для сопоставления колонок
class cell_matching():

    def __init__(self):
        #Индексы колонок
        self.num_pp = 0 #A(None если нет)
        self.name = 1#B
        self.position = 2#C
        self.ownflats_type = 3#D
        self.ownflats_owntype = 4#E
        self.ownflats_meters = 5#F
        self.ownflats_country = 6#G
        self.rentflats_type = 7#H
        self.rentflats_meters = 8#I
        self.rentflats_country = 9#J
        self.cars = 10#K
        self.money = 11#L
        self.source = 12#M
        #В некоторых файлах семейные связи отдельной колонкой
        self.family = None
        
        #Индекс первой строки с данными
        self.first_str = 1
        #Заполнение пустой колонки (иногда бывает прочерк)
        self.empty_cell = ""
        #range строк с заголовком 
        self.caption_str = range(0)
        #Количество колонок
        self.cells_count = 13
        #Список данных в одной ячейке (Word,Excel) взаимоискл. с multi_row_value
        self.list_in_cell = False
        #Одно значение в нескольких строках (Excel)
        self.multi_row_value = False
        #Сдвоенные колонки которые надо разделить
        self.split_cells =[]
        #Добавочные пустые колонки в конце
        self.extra_cells_intheend = range(0,1)
        #Добавлять колонки в индекс 
        self.insert_cells_ind = 8
        #Функция которая обрабатывает строку
        self.transform_function = None 
        
        

    def get_cell(self,cell_name,cell_list):
        cell_index = getattr(self, cell_name)
        if cell_index is None:
            return None
        elif isinstance(cell_index,list):
            value = None
            for ind in cell_index:
                value = cell_list[ind] if value is None else value + cell_list[ind]
            
            return value

        else:
            return cell_list[cell_index]

    def transform_row_1(self,row_list):
        #Приводит строку к длинне и 
        #Оставляет в строке только 
        #номер, имя должность доход источник (если находит)
        import re

        empty_row = ['']*self.cells_count

        if len(row_list)<4:
            return empty_row
        
        while len(row_list)>self.cells_count:
            del row_list[-1]

        family_pattern = re.compile(r'(Супруг)|(Несовершеннолетний)')
        num_pattern = re.compile(r'\d')
        name_pattern = re.compile(r"[А-ЯЁ][а-яё]*\.*\s+[А-ЯЁ]\.\s*[А-ЯЁ]\.")
        emptycell_pattern = re.compile(r'\s*'+self.empty_cell+r'\s*')
        
        num_pp = "".join(row_list[self.num_pp]).strip()
        name = "".join(row_list[self.name]).strip()
        
        if (
            (family_pattern.match(name) and num_pp == '')
            or 
            (name_pattern.match(name) and num_pattern.match(num_pp))
            ):
            
            empty_row[self.num_pp] = row_list[self.num_pp]
            empty_row[self.name] = row_list[self.name]
            empty_row[self.position] = row_list[self.position]
            
            for num in range(1,len(row_list)-self.position):
                if emptycell_pattern.fullmatch("".join( row_list[-num])):
                    empty_row[self.money] = row_list[-num-1]
                    empty_row[self.source] = row_list[-num]
                    break
                if num_pattern.match("".join(row_list[-num])):
                    empty_row[self.money] = row_list[-num]
                    break
        
        return empty_row

    def transform_row_2(self,row_list):
        #Приводит строку к длинне и 
        #Оставляет в строке только 
        #номер, имя должность доход источник (если находит)
        import re

        empty_row = ['']*self.cells_count

        if len(row_list)<4:
            return empty_row
        
        while len(row_list)>self.cells_count:
            del row_list[-1]

        family_pattern = re.compile(r'(Супруг)|(Несовершеннолетний)')
        num_pattern = re.compile(r'\d')
        name_pattern = re.compile(r"[А-ЯЁ][а-яё]*\.*\s+[А-ЯЁ]\.\s*[А-ЯЁ]\.")
        emptycell_pattern = re.compile(r'\s*'+self.empty_cell+r'\s*')
        
        #num_pp = "".join(row_list[self.num_pp]).strip()
        name = "".join(row_list[self.name]).strip()
        
        if (family_pattern.match(name)
            or name_pattern.match(name)):
            
            #empty_row[self.num_pp] = row_list[self.num_pp]
            empty_row[self.name] = row_list[self.name]
            empty_row[self.position] = row_list[self.position]
            
            for num in range(1,len(row_list)-self.position):
                cell_str = "".join(row_list[-num])
                #print(cell_str)
                
                if (emptycell_pattern.fullmatch(cell_str)
                    or re.search(r'сточник',cell_str)):
                    
                    if num_pattern.match("".join(row_list[-num-1])):
                        empty_row[self.money] = row_list[-num-1]
                        empty_row[self.source] = row_list[-num]
                    
                    break
                    
                if re.match(r'Россия',cell_str):
                    break
                
                if num_pattern.match(cell_str):
                    empty_row[self.money] = row_list[-num]
                    break
        
        return empty_row

    def transform_minstroy2013(self,row_list):
        import re
        
        empty_row = ['']*self.cells_count

        if len(row_list)<4:
            return empty_row
        
        while len(row_list)>self.cells_count:
            del row_list[-1]

        family_pattern = re.compile(r'(супруг)|(сын)|(дочь)')
        name_pattern = re.compile(r"[А-ЯЁ][а-яё]*\s+[А-ЯЁ][а-яё]*\s+[А-ЯЁ][а-яё]*")
        

        name = "".join(row_list[self.name]).strip()
        
        if name_pattern.match(name):

            empty_row[self.num_pp] = '1'
            empty_row[self.name] = row_list[self.name]
            empty_row[self.position] = row_list[self.position]
            empty_row[self.money] = row_list[self.money]

        elif family_pattern.match(name):

            empty_row[self.num_pp] = ''
            empty_row[self.name] = row_list[self.name]
            empty_row[self.position] = ''
            empty_row[self.money] = row_list[self.money]

        return empty_row

    def transform_mintrans2018(self,row_list):
        #Превращает доход в формате 1.000.000 в 1000000
        import re

        if len(row_list)<self.cells_count:
            return row_list
        
        
        row_list[self.money] = [re.sub(r'(\.|\.\s)(?=\d\d\d)','',money_str)
            for money_str in row_list[self.money]]

        #print('row_list : '+str(row_list))
        return row_list


    def transform_minenergo2014(self,row_list):
        #Разбивает ячейки на собственность и пользование
        import re

        #print('row_list : '+str(row_list))
        
        rentflat_pattern = re.compile('(пользование)')
        ownflat_pattern = re.compile('(собственность)')

        new_row = ['']*self.cells_count
        new_row[self.name] = row_list[self.name]
        new_row[self.position] = row_list[self.position]
        new_row[self.money] = row_list[self.money]
        new_row[self.cars] = row_list[6]
        new_row[self.source] = row_list[7]

        flat = ''.join(row_list[3])
        if rentflat_pattern.search(flat):
            new_row[self.rentflats_type] = [rentflat_pattern.sub('',flat),]
            new_row[self.rentflats_meters] = row_list[4]
            new_row[self.rentflats_country] = row_list[5]
        else:
            new_row[self.ownflats_type] = [ownflat_pattern.sub('',flat),]
            new_row[self.ownflats_owntype] = ['собственность',]
            new_row[self.ownflats_meters] = row_list[4]
            new_row[self.ownflats_country] = row_list[5]

        return new_row

    def transform_mcx2012(self,row_list):
        #Разбивает ячейки на cобственность , вид собственности 
        #и добавляет пустой мсточник
        
        #new_matching.ownflats_owntype = 10 #добавляется постобработкой
        #new_matching.source = 11 #добавляется постобработкой
        import re
        owntype_pattern = re.compile(r'(?<=\().*(?=\))')

        #print('row_list : '+str(row_list))
        
        ownflats_type = row_list[self.ownflats_type]
        if re.fullmatch(r'[\s'+self.empty_cell+r']*',ownflats_type):
            ownflats_owntype = ''
        elif owntype_pattern.search(ownflats_type):
            ownflats_owntype = owntype_pattern.search(ownflats_type).group(0)
            ownflats_type = re.sub(r'\('+ownflats_owntype+r'\)',' ',ownflats_type)
        else:
            ownflats_owntype = 'собственность'

        row_list[self.ownflats_type] = ownflats_type
        row_list.append(ownflats_owntype)
        row_list.append('')

        return row_list


