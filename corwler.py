# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 00:17:32 2018

@author: linzino
"""
import requests #引入函式庫
from bs4 import BeautifulSoup
import re
import json
import feedparser


def udn_news():
    '''
    抓最新前五篇新聞
    
    回傳是一個dict
    '''
    rss_url = 'https://udn.com/rssfeed/news/2/6638?ch=news'
 
    # 抓取資料
    rss = feedparser.parse(rss_url)
    
    cards = []    
    for index in range(0,5):
        # 抓文章標題
        title = rss['entries'][index]['title']
        # 抓文章連結
        link = rss['entries'][index]['link']
        # 處理摘要格式
        summary =  rss['entries'][index]['summary']
        
        if 'img' in summary:
            soup = BeautifulSoup(summary, 'html.parser')
            p_list = soup.find_all('p')
            # 抓文章摘要 限制只有60個字
            text = p_list[1].getText()[:50]
            # 抓文章圖片
            image = p_list[0].img['src']
        else:
            # 沒有圖片
            text = summary[:50]
            image = 'https://i.imgur.com/vkqbLnz.png'
        
        card = {'title':title,
                'link':link,
                'summary': text,
                'img':image
                }
        cards.append(card)
        
    return cards


def Dcard():
    '''
    在Dcard 上某個關鍵字最新的文章
    '''
    url = 'https://www.dcard.tw/search?query=%E5%8D%97%E5%B1%B1%E4%BA%BA%E5%A3%BD'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    atags = soup.findAll("a", {"class": "tgn9uw-3 ebwnQU"})
    pre_url = 'https://www.dcard.tw'
    
    string = '最新5篇Dcard貼文：\n'
    for  item in atags[:5]:
        string += item.text+'\n' + pre_url+item['href']+'\n'
    
    return string

def nanshan_news():
    '''
    南山官網最新五則新聞
    '''
    url = 'https://www.nanshanlife.com.tw/NanshanWeb/news/174/pagination/0'
    resp = requests.get(url)
    title = re.findall(r'title":(.*?),', resp.text)
    number = re.findall(r'id":(.*?),', resp.text)
    ur = "https://www.nanshanlife.com.tw/NanshanWeb/news/174/"
    string = '最新5篇南山新聞：\n'
    for t, num in zip(title[:5], number[:5]):
        t = t.replace('"', "")
        string += t + '\n' + ur + 'd/' + num + '\n'
    
    return string

def weather():
    '''
    中央氣象局雷達回波圖
    '''
    url = 'https://www.cwb.gov.tw/Data/js/obs_img/Observe_radar.js'
    imgs = re.sub('"', '', requests.get(url).text)
    img = re.findall(r'{img:(.*?),', imgs)
    text = img[0].replace("'", "")
    radar_url = "https://www.cwb.gov.tw/Data/radar/" + text
    
    return radar_url

def cna():
    '''
    中央社新聞
    '''
    rss_url = 'http://feeds.feedburner.com/cnaFirstNews'
    # 抓取資料
    rss = feedparser.parse(rss_url)
    dic = []    
    for index in range(0,5):
        # 抓文章標題
        title = rss['entries'][index]['title']
        # 抓文章連結
        link = rss['entries'][index]['link']
        # 處理摘要格式
        text =  rss['entries'][index]['summary'].split('<br')[0][:50]
        card = {'title':title,
                'link':link,
                'summary': text
                }
        dic.append(card)
        
    return dic

def nanshan_product():
    '''
    南山商品
    '''
    url = 'https://www.nanshanlife.com.tw/NanshanWeb/static-sidebar/8'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    atags = soup.findAll("span", {"class": "clr-fff"})
    nums = ['10', '17', '24', '35', '272', '310', '49', '60', '424', '307']
    urls = ['https://www.nanshanlife.com.tw/NanshanWeb/product/' + i for i in nums]
    other = ['https://www.nanshanlife.com.tw/promotion/travel/index.htm', 'http://ilp.nanshanlife.com.tw/']
    urls += [i for i in other] 
    dic = []    
    for index, url in zip(range(0, 12), urls):
        # 處理摘要格式
        card = {'title':atags[index].text.replace('\n        ',''),
                'link':url
#                , 'summary': text
                }
        dic.append(card)
        
    return dic

    


    