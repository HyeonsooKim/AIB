import os

import pandas as pd
import requests
import sqlite3
import urllib.request as req

from bs4 import BeautifulSoup
from html_table_parser import parser_functions as parser


def load_stock_list():
    conn = sqlite3.connect("project3.sqlite3")
    cur = conn.cursor()

    cur.execute("""SELECT * FROM Stock_list;""")
    stock_list = cur.fetchall()

    columns = ['인덱스', '종목명', '종목코드', '상장시장']
    stock_list = pd.DataFrame(stock_list, columns=columns).drop('인덱스', axis=1)

    #종목코드 0번째 - 삼성전자
    sample_code = stock_list.loc[0,'종목코드']

    return sample_code


def samsung_stock_price(sample_code):
    #데이터를 긁어옴 - 모듈 사용
    # sample = fdr.DataReader(sample_code, start = start_date, end = end_date)[['Close']].reset_index()


    # 웹 크롤링
    # 2021년 1월 7일, 네이버가 웹크롤링 차단 실시
    # 네이버 금융서버에서 http 패킷 헤더의 웹 브라우저 정보(User-agent)를 체크
    # 웹 브라우저 정보를 함께 전송해야 함
    url = f'https://finance.naver.com/item/sise_day.nhn?code={sample_code}&page=1'
    with requests.get(url, headers={'User-agent': 'Mozilla/5.0'}) as doc: # <== 이처럼 브라우저 정보를 requests 모듈을 이용해 전송해야 한다.
        # print("doc.text: ", doc.text)
        html = BeautifulSoup(doc.text, "lxml")
        # print("html: ", html)
        pgrr = html.find('td', class_='pgRR')
        # print("pgrr", pgrr)
        s = str(pgrr.a['href']).split('=')
        # print("s: ", s)
        #마지막 페이지
        last_page = s[-1]
        # print(last_page)
        # breakpoint()


    df = pd.DataFrame()
    sise_url = f'https://finance.naver.com/item/sise_day.nhn?code={sample_code}'

    for page in range(1, int(last_page)+1):
        page_url = '{}&page={}'.format(sise_url, page)
        response_page = requests.get(page_url, headers={'User-agent': 'Mozilla/5.0'}).text
        df = df.append(pd.read_html(response_page)[0])

        
    df = df.dropna() # n/a 제거
    df = df.reset_index(drop=True) # 인덱스 리셋
    #종가와 날짜 제외 모두 버림
    df = df.drop(columns=['전일비', '시가', '고가', '저가', '거래량'])
    #2021년 날짜만 사용
    df = df[df['날짜']>"2021.01.01"]
    df = df.rename(columns={'날짜':'Date', '종가':'Close'})
    df = df.sort_values(by='Date').reset_index(drop=True) # 인덱스 리셋
    df['Date'] = pd.to_datetime(df['Date'])

    return df

def to_pivot(df):

    #시작과 끝날짜
    start_date = '20210104'
    end_date = '20211010'
    #월 - 0, 화 - 1, 수 - 2, 목 - 3, 금 - 4
    start_weekday = pd.to_datetime(start_date).weekday()
    #끝 날짜의 주를 52주에서 센 값
    max_weeknum = pd.to_datetime(end_date).strftime('%V')
    #총 영업일 날짜 수
    Business_days = pd.DataFrame(pd.date_range(start_date,end_date,freq='B'), columns = ['Date'])

    #데이터를 비즈니스데이와 outer join(합집합)
    sample = pd.merge(Business_days, df, how = 'outer')
    #sample에 weekday 열 추가
    sample['weekday'] = sample.Date.apply(lambda x : x.weekday())
    #sample weeknum은 2021년에서 몇번 째 주인지 알려주기 위함
    sample['weeknum'] = sample.Date.apply(lambda x : x.strftime('%V'))
    #결측치는 앞의 데이터로 채움, 뒤의 데이터로 채울 시에는 bfill 사용
    sample.Close = sample.Close.ffill()
    #index(행 위치에 들어갈 열), columns(열 위치에 들어갈 열), values(데이터로 사용할 열)
    sample = pd.pivot_table(data = sample, values = 'Close', columns = 'weekday', index = 'weeknum')

    return sample

def stock_price_save(df):

    conn = sqlite3.connect("project3.sqlite3")
    cur = conn.cursor()

    cur.execute("""DROP TABLE IF EXISTS Stock_info""")
    cur.execute("""CREATE TABLE Stock_info (
                id INTEGER PRIMARY KEY NOT NULL,
                Date VARCHAR,
                Close INTEGER
    );""")

    for i in range(len(df)):
        cur.execute("""INSERT INTO Stock_info (Date, Close) VALUES (?, ?);""", (str(df['Date'][i]), df['Close'][i]))

    conn.commit()


sample_code = load_stock_list()
df = samsung_stock_price(sample_code)
sample = to_pivot(df)
stock_price_save(df)





