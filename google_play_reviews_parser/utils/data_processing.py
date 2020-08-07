#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def clear_request_data(text):
    '''
    Clear text from post request,
    that help to make list from text
    '''

    text = text[4:]

    text = re.sub(r''''*\\"''', "'''", text)
    text = re.sub(r'\\n', '', text)
    # text = text.replace('\\', '\\\\')
    text = re.sub('null', 'None', text)
    text = re.sub('false', 'False', text)
    text = re.sub('true', 'True', text)

    return text


def make_request_data(text):
    '''
    Make reviews list from cleared text
    '''
    text = clear_request_data(text)
    data = eval(text)

    try:
        data = eval(data[0][2])
    except ValueError:
        print('Cant extract reviews info for this data')
        return None

    return data


def get_token_from_text(text):
    '''
    Extract token from no-cleared text
    Using if request text is not valid
    to continue parsing other reviews
    '''
    token = re.findall(r'\\"(C[^"]+(?:Mg|Yy|jI))\\"\]', text)
    if len(token) == 1:
        return token[0]
    else:
        print('Token not extractable')
        # if input('Do you want to watch text from request?[y/n]') == 'y':
        #     print(text)
        return None
