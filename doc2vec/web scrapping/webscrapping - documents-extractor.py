from bs4 import BeautifulSoup
import en_core_web_sm
nlp = en_core_web_sm.load()
from pandas import DataFrame
import multiprocessing
from csv import writer
import pandas as pd
import validators
import sys, traceback
import requests
import spacy
import time
import csv
import ast
import re

documents_completed = []
documents_incomplete = []

def Scraping(urls):
    '''
    Function: Takes the url given and extracts the document from different tags in the html format.
    '''
    
    try:
        global case_doc_content
        website_url = requests.get(urls).text
        soup = BeautifulSoup(website_url, 'html.parser')
        case_docs =[]
        class_types = ['pro-indent', 'bodytext', 'sylct-f jy-both', 'SYLCTF']
        for class_type in class_types:
            content_tags = soup.find_all('p', class_=class_type)
            if content_tags:
                for tag in content_tags:
                    case_docs.append(text_cleansing(tag.text))
                case_doc_content = ' '.join(case_docs)
        
        # Change the file destination as per your choice
        with open(r'Scrapped_docs.csv','a',newline='') as f:
            writer=csv.writer(f)
            writer.writerow([case_doc_content])
                        
        documents_completed.append('Processed - '+urls)
            
        return documents_completed
        
    except Exception as e:
            
        documents_incomplete.append('Unprocessed -'+urls)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback_details = {
                         'filename': exc_traceback.tb_frame.f_code.co_filename,
                         'lineno'  : exc_traceback.tb_lineno,
                         'name'    : exc_traceback.tb_frame.f_code.co_name,
                         'type'    : exc_type.__name__,
                         'message' : exc_traceback._some_str(), 
                        }
        pass
        return documents_incomplete, traceback_details
    