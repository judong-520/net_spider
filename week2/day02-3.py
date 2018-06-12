from urllib.error import URLError
from urllib.request import urlopen

import re

import pymysql
from pymysql import Error


def decode_page(page_bytes, charsets=('utf-8',)):
    page_html = None
    for charset in charsets:
        try:
            page_html = page_bytes.decode(charset)
        except UnicodeDecodeError:
            pass
    return page_html


def get_page_html(seed_url, *, retry_times=3, charsets=('utf-8',)):
    page_html = None
    try:
        page_html = decode_page(urlopen(seed_url).read(), charsets)
    except URLError:
        if retry_times > 0:
            return get_page_html(seed_url, retry_times=retry_times-1, charsets=charsets)
    return page_html


def get_matched_part(page_html, pattern_str, igorance=re.I):
    pattern_regex = re.compile(pattern_str, igorance)
    return pattern_regex.findall(page_html) if page_html else []


def start_crawl(seed_url, match_pattern, *, max_depth=-1):
    conn = pymysql.connect(host='localhost', port=3306,
                           database='crawler', user='root',
                           password='456654', charset='utf8')
    try:
        with conn.cursor() as cursor:
            url_list = [seed_url]
            visited_url_list = {seed_url: 0}
            while url_list:
                current_url = url_list.pop(0)
                depth = visited_url_list[current_url]

    except Error:
        pass




