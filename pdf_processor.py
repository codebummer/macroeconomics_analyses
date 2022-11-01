
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
        # self.df = []
        
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
        # excerpt = text[start+2:end-2]
        # brokendown = []
        # added = ''
        # for element in excerpt:
        #     asc = ord(element)
        #     if 12593 <= asc and asc <= 52044:
        #         brokendown += added
        #         added = ''
        #     else:
        #         added += element
        
        excerpt = text[start+2:end-2].replace('\n', ' ').strip().split(' ')                  
        # for element in excerpt:
        #     excerpt_stripped += element.replace('\n', '')
        # excerpt = [i.split('\n') for i in excerpt]
      
        brokendown = []
        added = []
        for element in excerpt:
            asc = ord(element[0])
            if 12593 <= asc and asc <= 52044:                
                brokendown.append(added)
                added = [element]
            else:
                added.append(element) 
        
        extracted = pd.DataFrame([])
        for num, element in enumerate(brokendown):
            if num is 0:
                extracted['Month'] = element
            # col_name = [element[0].strip()]
            # col = element[1:]
            else:
                extracted[element[0]] = element[1:]
            
                        
        # print(extracted)
        return extracted

sep22 = locator('2022년 9월 수출입동향.pdf', '월별 수출실적', '%)', '수출액 및')
