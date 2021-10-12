import pandas as pd
import xlrd
import sqlite3
import os


#부동산 정보 저장용 - 안씀
# df = pd.read_excel("Area_Code.xls")

# df = pd.DataFrame(df).reset_index(drop=False)

# conn = sqlite3.connect("project3.sqlite3")

# cur = conn.cursor()

# cur.execute("""DROP TABLE IF EXISTS AreaCode;""")
# cur.execute("""CREATE TABLE AreaCode(
#                id INTEGER PRIMARY KEY NOT NULL,
#                Areacode_in_law VARCHAR,
#                Name VARCHAR,
#                Abolition VARCHAR);""")

# for i in range(len(df)):
#     cur.execute("""INSERT INTO AreaCode (id, Areacode_in_law, Name, Abolition) VALUES (?, ?, ?, ?);""", (i, str(df['법정동코드'][i]), df['법정동명'][i], df['폐지여부'][i]))

# conn.commit()


#주식종목코드 저장용
path = './'
list_name = 'Stock_List.csv'
sample_name = 'sample_submission_week4.csv'

stock_list = pd.read_csv(os.path.join(path,list_name))
stock_list['종목코드'] = stock_list['종목코드'].apply(lambda x : str(x).zfill(6))

conn = sqlite3.connect("project3.sqlite3")

cur = conn.cursor()

cur.execute("""DROP TABLE IF EXISTS Stock_list;""")
cur.execute("""CREATE TABLE Stock_list (
               id INTEGER PRIMARY KEY NOT NULL,
               Name VARCHAR,
               Code VARCHAR,
               Market VARCHAR
);""")

for i in range(len(stock_list)):
    cur.execute("""INSERT INTO Stock_list (Name, Code, Market) VALUES (?,?,?);""", (stock_list['종목명'][i], stock_list['종목코드'][i], stock_list['상장시장'][i]))

conn.commit()