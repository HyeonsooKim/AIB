from bs4 import BeautifulSoup
import urllib.request as req
import requests
from html_table_parser import parser_functions as parser
import pandas as pd

# sample_code = '005930'
# url = "https://finance.naver.com/item/sise_day.nhn?code={sample_code}"
# res = req.urlopen(url).read().decode('cp949')
# # res = req.urlopen(url).read()
# soup = BeautifulSoup(res, 'html.parser')

# a = soup.find_all(table)
# print(a)

# 2. 웹 크롤링
# 2021년 1월 7일, 네이버가 웹크롤링 차단 실시
# 네이버 금융서버에서 http 패킷 헤더의 웹 브라우저 정보(User-agent)를 체크
# 웹 브라우저 정보를 함께 전송해야 한다.
url = 'https://finance.naver.com/item/sise_day.nhn?code=005930&page=1'
with requests.get(url, headers={'User-agent': 'Mozilla/5.0'}) as doc: # <== 이처럼 브라우저 정보를 requests 모듈을 이용해 전송해야 한다.
    html = BeautifulSoup(doc.text, "lxml")
    pgrr = html.find('td', class_='pgRR')
    s = str(pgrr.a['href']).split('=')
    last_page = s[-1]
    print(last_page)


df = pd.DataFrame()
sise_url = 'https://finance.naver.com/item/sise_day.nhn?code=005930'

for page in range(1, int(last_page)+1):
    page_url = '{}&page={}'.format(sise_url, page)
    response_page = requests.get(page_url, headers={'User-agent': 'Mozilla/5.0'}).text
    df = df.append(pd.read_html(response_page)[0])

df = df.dropna() # n/a 제거
df = df.reset_index(drop=True) # 인덱스 리셋
df = df.drop(columns=['전일비', '시가', '고가', '저가', '거래량'])
print(df)