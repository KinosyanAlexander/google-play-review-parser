#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from google_play_reviews_parser import Reviews

class TestScore:
    reviews = Reviews('jp.co.ponos.korogarimasu', lang='ru')

    def test_score_1(self):
        self.reviews.refresh()
        self.reviews.score = 1
        self.reviews.change_count(5000)
        data = self.reviews.get_reviews()
        data = list(map(lambda x: x.score == 1, data))

        assert all(data)
    
    def test_score_2(self):
        self.reviews.refresh()
        self.reviews.score = 2
        self.reviews.change_count(5000)
        data = self.reviews.get_reviews()
        data = list(map(lambda x: x.score == 2, data))
        
        assert all(data)

    def test_score_3(self):
        self.reviews.refresh()
        self.reviews.score = 3
        self.reviews.change_count(5000)
        data = self.reviews.get_reviews()
        data = list(map(lambda x: x.score == 3, data))
        
        assert all(data)
    
    def test_score_4(self):
        self.reviews.refresh()
        self.reviews.score = 4
        self.reviews.change_count(5000)
        data = self.reviews.get_reviews()
        data = list(map(lambda x: x.score == 4, data))
        
        assert all(data)
    
    def test_score_5(self):
        self.reviews.refresh()
        self.reviews.score = 5
        self.reviews.change_count(5000)
        data = self.reviews.get_reviews()
        data = list(map(lambda x: x.score == 5, data))
        
        assert all(data)
    
    def test_score_1_2_3(self):
        self.reviews.refresh()
        self.reviews.score = [1, 2, 3]
        self.reviews.change_count(5000)
        data = self.reviews.get_reviews()
        data = list(map(lambda x: x.score in [1, 2, 3], data))
        
        assert all(data)

    def test_score_5_1_4_3(self):
        self.reviews.refresh()
        self.reviews.score = [5, 1, 4, 3]
        self.reviews.change_count(5000)
        data = self.reviews.get_reviews()
        data = list(map(lambda x: x.score in [1, 3, 4, 5], data))
        
        assert all(data)

class TestBigData:
    reviews = Reviews('org.telegram.messenger', start_token=None, lang='en', sqlbase='telegram_large_base_2.db')

    def test_count_1m(self):
        # self.reviews.refresh()
        self.reviews.change_count(1 * (10 ** 6))
        try:
            data = self.reviews.get_reviews()
        except Exception as e:
            print(self.reviews.token)
            print(e)
            data = []

        assert len(data) == (1 * (10 ** 6))


if __name__ == "__main__":
    h = TestBigData()
    h.test_count_1m()
