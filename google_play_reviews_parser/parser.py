#!/usr/bin/env python
# -*- coding: utf-8 -*-
from requests import post
import time
import re
import sqlite3 as sq

from google_play_reviews_parser.constants import Url, PostData
from google_play_reviews_parser.utils import make_request_data, Review, get_token_from_text

# from constants import Url, PostData
# from utils import make_request_data, clear_request_data, Review, get_token_from_text



class Reviews():
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
        self.all_count = count
        self.count = self.all_count % 199
        if not self.count:
            self.count = 199
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
        
    
    def request(self):
        request = post(self.url,
                    data=self.post_data,
                    headers={"content-type": "application/x-www-form-urlencoded"}
                )
        return request

    def format_post_data(self, is_start=False):
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
        data = make_request_data(request.text)
        return data
    
    def create_base(self, filename=''):
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
        try:
            data = map(lambda x: x.get_list(), data)
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

    def get_reviews(self):
        self.play_parsing = True

        request = self.request()

        try:
            data = self.extract_request_data(request)
            reviews_data = data[0]
        except (SyntaxError, ValueError, TypeError):
            token = get_token_from_text(request.text)
            if token:
                print(self.token)
                self.token = token
                print('\n\nnew_token\n\n', self.token)
                self.count = 199
                self.format_post_data()
                return self.get_reviews()
            else:
                print('Sorry, something get wrong with extracting data\n')
                print(self.token)
                print('\nfrom this token you can start parsing, when this issue fixes')
                # if input('Do you want to watch text? [y/n]') == 'y':
                #     print(clear_request_data(request.text))
                print('That is over, token cant be extracted')
                return self.data

        reviews = list(map(self.make_review, reviews_data))
        reviews = list(filter(lambda x: x, reviews))
        self.data += reviews

        if self.sqlbase:
            self.add_reviews_to_base(reviews)

        if len(self.data) >= self.all_count:
            self.play_parsing = False
            print(f'All {len(self.data)} reviews parsed')

        try:
            self.token = data[1][1]
        except IndexError:
            if data:
                print(f'Reviews are over, there are only {len(self.data)} reviews')
                self.count = 0
                self.play_parsing = False
        
        if self.play_parsing:
            print(f'{len(self.data)}   reviews parsed')
            self.count = 199
            self.format_post_data()
            return self.get_reviews()
        else:
            return self.data




if __name__ == "__main__":
    pass