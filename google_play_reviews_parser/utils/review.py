#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time


class Review():
    '''
    Review class, that contains
    main info about review
    '''
    def __init__(self,
                nickname,
                review_text,
                score,
                likes,
                date
                ):
        self.nick = nickname
        self.text = review_text
        self.score = score
        self.likes = likes
        self.date = date
    
    def __repr__(self):
        return f'<Review\n nick: {self.nick}\n text: {self.text}\n score: {self.score}\n likes: {self.likes}\n date: {self.date}\n>'

    def get_list(self, for_base=False):
        '''
        return list of review parameters
        if flag "for_base" is True,
        date in list will be like %d/%m/%Y format
        else time.datetime object
        '''
        if for_base:
            try:
                date = time.strftime('%d/%m/%Y', self.date)
            except TypeError:
                return None
        else:
            date = self.date

        return [self.nick, self.text, self.score, self.likes, date]

if __name__ == "__main__":
    pass
