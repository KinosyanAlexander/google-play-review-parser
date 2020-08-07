#!/usr/bin/env python
# -*- coding: utf-8 -*-

class PostData():
    '''
    Data to post for extracting reviews
    '''
    POST_DATA_FOR_FIRST_REQUEST = "f.req=%5B%5B%5B%22UsvDTd%22%2C%22%5Bnull%2Cnull%2C%5B2%2C{sort}%2C%5B{count}%2Cnull%2Cnull%5D%2Cnull%2C%5Bnull%2C{score}%5D%5D%2C%5B%5C%22{app_id}%5C%22%2C7%5D%5D%22%2Cnull%2C%22generic%22%5D%5D%5D"
    POST_DATA_FOR_PAGINATED_PAGE = "f.req=%5B%5B%5B%22UsvDTd%22%2C%22%5Bnull%2Cnull%2C%5B2%2C{sort}%2C%5B{count}%2Cnull%2C%5C%22{token}%5C%22%5D%2Cnull%2C%5Bnull%2C{score}%5D%5D%2C%5B%5C%22{app_id}%5C%22%2C7%5D%5D%22%2Cnull%2C%22generic%22%5D%5D%5D"