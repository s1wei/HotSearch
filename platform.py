# !/usr/bin/python3
# _*_ coding: utf-8 _*_
"""
Copyright (C) 2024 - s1wei.com, Inc. All Rights Reserved

@Time    : 2024/4/26 17:08:49
@Author  : s1wei
@Email   : admin@s1wei.com
@Blog    : https://www.denceun.cn/author/1/
@File    : platform.py
@IDE     : PyCharm
"""

import json

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

# 微博官方接口
def weibo():

    url = 'https://weibo.com/ajax/side/hotSearch'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.text
        response_data = json.loads(data)
        realtime_data = response_data["data"]["realtime"]

        # sorted_data = sorted(realtime_data, key=lambda x: int(x.get("raw_hot", 0)), reverse=True)

        for index, entry in enumerate(realtime_data, start=1):
            print(f"{index}. {entry.get('word', 'Unknown')} - {entry.get('raw_hot', 'Unknown')}\n"
                  f"  URL: https://s.weibo.com/weibo?q={quote(entry.get('word', 'Unknown'))}")

# 百度官方接口
def baidu():

    url = 'https://top.baidu.com/board?tab=realtime'
    response = requests.get(url)

    if response.status_code == 200:

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all category-wrap_iQLoo items
        category_items = soup.find_all('div', {'class': 'category-wrap_iQLoo'})

        # Initialize a list to store the extracted data
        hot_search_data = []

        # Iterate over category-wrap_iQLoo items and extract relevant information
        for item in category_items:
            index = item.find('div', {'class': 'index_1Ew5p'}).get_text(strip=True)
            hot_score = item.find('div', {'class': 'hot-index_1Bl1a'}).get_text(strip=True)
            title = item.find('div', {'class': 'c-single-text-ellipsis'}).get_text(strip=True)

            hot_search_data.append({'index': index, 'hotScore': hot_score, 'title': title})

        # print(hot_search_data)

        for index, hot_search in enumerate(hot_search_data, start=1):
            print(f"{index}. {hot_search['title']} - {hot_search['hotScore']}\n"
                  f"  URL: https://new.qq.com/search?query={quote(hot_search['title'])}")

# 腾讯官方接口
def tengxun():

    url = 'https://i.news.qq.com/web_backend/getHotQuestionList'
    response = requests.get(url)

    if response.status_code == 200:
        # print(response.text)

        data = response.text

        response_data = json.loads(data)

        hot_questions = response_data['data']['hot_questions']

        # Iterating through hot questions
        for index, hot_question in enumerate(hot_questions, start=1):
            print(f"{index}. {hot_question['title']} - {hot_question['approve_num']} approvals\n"
                  f"  URL: https://new.qq.com/search?query={quote(hot_question['title'])}")

# 今日头条官方接口
def toutiao():

    url = 'https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc'
    response = requests.get(url)

    # print(response.text)

    if response.status_code == 200:

        data = response.text

        response_data = json.loads(data)

        hot_board = response_data['data']

        for index, hot_event in enumerate(hot_board, start=1):
            print(f"{index}. {hot_event['Title']} - {hot_event['HotValue']}\n"
                  f"  URL: https://so.toutiao.com/search?dvpf=pc&source=input&keyword={quote(hot_event['Title'])}")

# 知乎官方接口
def zhihu():

    url = 'https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true'
    response = requests.get(url)

    # print(response.text)
    #
    if response.status_code == 200:

        data = response.text

        response_data = json.loads(data)

        hot_lists = response_data['data']

        for index, hot_list in enumerate(hot_lists, start=1):
            print(f"{index}. {hot_list['target']['title']} - {hot_list['detail_text']}\n"
                  f"  URL: https://www.zhihu.com/search?type=content&q={quote(hot_list['target']['title'])}")

# 澎湃官方接口
def penggpai():

    url = 'https://cache.thepaper.cn/contentapi/wwwIndex/rightSidebar'
    response = requests.get(url)

    # print(response.text)
    #
    if response.status_code == 200:

        data = response.text

        response_data = json.loads(data)

        hotNews = response_data['data']['hotNews']
        # print(hotNews)

        for index, hotNew in enumerate(hotNews, start=1):
            print(f"{index}. {hotNew['name']} - {hotNew['praiseTimes']} 点赞\n"
                  f"  URL: https://www.thepaper.cn/newsDetail_forward_{quote(hotNew['contId'])}")

# 第三方接口
def weixin():

    url = 'https://tophub.today/n/WnBe01o371'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
    }
    response = requests.get(url, headers=headers)

    # print(response.text)

    if response.status_code == 200:
        # print(response.text)
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        today_content = soup.find('div', class_='cc-dc')
        # print(today_content)
        # Find all category-wrap_iQLoo items
        articles = []
        #
        # # Extract information from each article
        for article in today_content.find_all('tr'):
            title_elem = article.find('td', {'class': 'al'}).find('a')
            # print(title_elem)
            title = title_elem.text.strip()
            href = title_elem.get('href')
            reads = article.find_all('td')[-2].text.strip().split()[0]

            articles.append({
                'title': title,
                'href': href,
                'reads': reads  # convert to int, handle 'W+' notation
            })

            # print(title)

        # print(articles)

        for index, article in enumerate(articles, start=1):
            print(f"{index}. {article['title']} - {article['reads']}\n"
                  f"  URL: https://new.qq.com/search?query={article['href']}")

# 抖音需要登录拿cookie才能，这里就不做了
def douyin():

    url = 'https://www.douyin.com/aweme/v1/web/hot/search/list/'
    headers = {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        'Cookie': '抖音需要登录拿cookie才能，这里就不做了'
    }
    response = requests.get(url, headers=headers)

    print(response.text)

    # if response.status_code == 200:
    #
    #     data = response.text
    #
    #     response_data = json.loads(data)
    #
    #     # trending_lists = response_data['data']['trending']
    #     word_lists = response_data['data']['word_list']
    #     print(word_lists)


