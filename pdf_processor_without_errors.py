import os
import PyPDF2
import math
import pandas as pd


class locator:
    def __init__(self, filename, find_word, find_start, find_end):
        '''
        filename: a name of a file you want to read
        find_word: a word by which you find the page you're interested in
        find_start: a character you want to start extracting from
        find_end: a character you want to end extracting until
        '''
        path = 'D:/myprojects/macroeconomics_analyses/'
        self.pdf_object = open(path+filename, 'rb')
        self.pdf_read = PyPDF2.PdfFileReader(self.pdf_object)
        self.ISEXPORT = True
        if find_word != '월별 수출실적':
            self.ISEXPORT = False
               
        print(self.ISEXPORT)
        
        for page in range(self.pdf_read.numPages):
            page_object = self.pdf_read.getPage(page)
            text = page_object.extractText()
            index = text.find(find_word)
            if index is not -1:
                self.df = self.page_processor(page, find_start, find_end)
        
        print(self.df)
    
    def page_processor(self, page, find_start, find_end):
        text = self.pdf_read.getPage(page).extractText()
        start = text.find(find_start)
        end = text.find(find_end)
        
        if self.ISEXPORT is True:
            excerpt = text[start+2:end-2].replace('\n', ' ').strip().split(' ')                  
        else:
            excerpt = text[start:end-2].replace('\n', '').strip().split(' ')

        brokendown = []
        added = []
        for element in excerpt:
            asc = ord(element[0]) 
            if 12593 <= asc and asc <= 52044:
                if self.ISEXPORT is True:                
                    brokendown.append(added)
                    added = [element]
                else:
                    
            else:
                added.append(element) 
        
        extracted = pd.DataFrame([])
        for num, element in enumerate(brokendown):
            if num is 0 and self.ISEXPORT is True:
                extracted['월'] = element

            else:
                extracted[element[0]] = element[1:]            
                        
        return extracted

sep22_export = locator('2022년 9월 수출입동향.pdf', '월별 수출실적', '%)', '수출액 및')
sep22_import = locator('2022년 9월 수출입동향.pdf', '월별 수입실적', '%)', '연간 수입액 및')
