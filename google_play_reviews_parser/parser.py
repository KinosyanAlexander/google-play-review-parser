#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import time
import re
import sqlite3 as sq

from google_play_reviews_parser.constants import Url, PostData
from google_play_reviews_parser.utils import make_request_data, Review, get_token_from_text

# from constants import Url, PostData
# from utils import make_request_data, clear_request_data, Review, get_token_from_text



class Reviews():
    '''
    Class, wich allow parse reviews
    and write reviews in sqlite base
    '''
    def __init__(self,
                app_id,
                lang='ru',
                count=1,
                score='null',
                sort='null',
                start_token=None,
                sqlbase=None):
        self.app_id = app_id
        self.lang = lang
        self.change_count(count)
        self.score = score
        self.sort = sort
        self.token = start_token
        self.sqlbase = sqlbase
        self.data = []

        self.url = Url.API_URL.format(lang=self.lang)

        self.format_post_data(is_start=not start_token)

        self.play_parsing = False

        if self.sqlbase:
            self.create_base()
    
    def change_count(self, count):
        '''
        Change count of reviews
        '''
        self.all_count = count
        self.count = count % 199
        if not self.count:
            self.count = 199
    
    def refresh(self):
        '''
        Restart info about Review
        '''
        self.data = []
        self.token = None
        self.play_parsing = False
        self.change_count(self.all_count)
        self.format_post_data(is_start=not self.token)
        self.url = Url.API_URL.format(lang=self.lang)
        if self.sqlbase:
            self.create_base()
    
    def change_lang(self, lang):
        '''
        Change reviews language
        '''
        self.lang = lang
        self.url = Url.API_URL.format(lang=self.lang)
    
    def request(self):
        '''
        Make post request to take reviews
        '''
        try:
            request = requests.post(self.url,
                        data=self.post_data,
                        headers={"content-type": "application/x-www-form-urlencoded"},
                        timeout=0.5
                    )
            return request
        except requests.exceptions.RequestException:
            try:
                return self.request()
            except RecursionError:
                return None

    def format_post_data(self, is_start=False):
        '''
        Formatting post data to make request
        '''
        if self.score is None:
            self.score = 'null'
        if self.sort is None:
            self.sort = 'null'

        if is_start:
            self.post_data = PostData.POST_DATA_FOR_FIRST_REQUEST.format(
                sort=self.sort,
                count=self.count,
                score=self.score,
                app_id=self.app_id
            )
        else:
           self.post_data = PostData.POST_DATA_FOR_PAGINATED_PAGE.format(
                sort=self.sort,
                count=self.count,
                token=self.token,
                score=self.score,
                app_id=self.app_id
            )
        return self.post_data
    
    def extract_request_data(self, request):
        '''
        Extracting reviews data from post request from self.request()
        '''
        data = make_request_data(request.text)
        return data
    
    def create_base(self, filename=''):
        '''
        Create Sqlite db for reviews
        '''
        if not self.sqlbase:
            self.sqlbase = filename if filename else f'{self.app_id}_base'
        
        self.conn = sq.connect(self.sqlbase)
        self.cursor = self.conn.cursor()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS
                               reviews
                               (nickname varchar(100),
                               text varchar,
                               score int,
                               likes int,
                               date date)
                               """)
        
        self.conn.commit()
    
    def add_reviews_to_base(self, data):
        '''
        Adding reviews from data (=> List of Review) to sqlite base
        if base exists
        '''
        try:
            data = map(lambda x: x.get_list(for_base=True), data)
            data = list(filter(lambda x: x, data))
            self.cursor.executemany('''
                   INSERT INTO reviews VALUES
                   (?,?,?,?,?)
                   ''', data)
            self.conn.commit()
            return True
        except AttributeError:
            print('Sql Base not exists')
            return False

    def make_review(self, element):
        '''
        Make Review() object from review info data
        '''
        nick = element[1][0]
        text = element[4]
        score = element[2]
        likes = element[6]
        try:
            date = time.gmtime(element[5][0])
        except TypeError:
            return None
        review = Review(nick, text, score, likes, date)

        return review

    def take_some_reviews(self):
        '''
        Func, that allow ONE request parsing
        '''
        self.play_parsing = True

        if not self.token:
            self.format_post_data(is_start=True)
        else:
            self.format_post_data(is_start=False)

        request = self.request()

        try:
            data = self.extract_request_data(request)
            reviews_data = data[0]
        except (SyntaxError, ValueError, TypeError):
            token = get_token_from_text(request.text)
            if token:
                self.token = token
                print('\n\nnew_token\n\n', self.token)
                self.format_post_data()
                return self.token
            else:
                print('Sorry, something get wrong with extracting data\n')
                print(self.token)
                print('\nfrom this token you can start parsing, when this issue fixes')
                # if input('Do you want to watch text? [y/n]') == 'y':
                #     print(clear_request_data(request.text))
                print('That is over, token cant be extracted')
                self.play_parsing = False
                return self.data
        
        reviews = list(map(self.make_review, reviews_data))
        reviews = list(filter(lambda x: x, reviews))
        
        if self.sqlbase:
            try:
                self.add_reviews_to_base(reviews)
                self.data += reviews
            except UnicodeEncodeError:
                print('Problem with data coding')
                pass

        if len(self.data) >= self.all_count:
            self.play_parsing = False
            print(f'All {len(self.data)} reviews parsed')
            return self.data

        try:
            self.token = data[1][1]
        except IndexError:
            if data:
                print(f'Reviews are over, there are only {len(self.data)} reviews')
                self.count = 0
                self.play_parsing = False
        
        if self.play_parsing:
            print(f'{len(self.data)}   reviews parsed')
            if (self.all_count - self.count) % 199:
                self.count = 199
    
    def get_reviews(self):
        '''
        Main func, that allow MANY requests parsing
        and fill self.data for reviews for self.all_count count
        '''
        self.play_parsing = True
        while self.play_parsing:
            self.take_some_reviews()
        
        self.token = None
        return self.data
    




if __name__ == "__main__":
    pass