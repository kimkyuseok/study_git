# csv 파일을 가지고 원하는 데이터 가져 오는 연습
# http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201030301
import csv
import os
from datetime import datetime

folder_path = r'D:\test\chackUS\study_git\95_csv\csv'
file_name = 'data_3910_20240614.csv'
full_file_path = os.path.join(folder_path, file_name)

with open(full_file_path, 'r') as file:
    reader = csv.DictReader(file)
    data = [{k: v for k, v in row.items()} for row in reader]
    # print(data)
    # 종목명에 '코스피200'이 들어간 항목을 찾아서 따로 추출
    kospi_200_data = [row for row in data if '코스피 200' in row['기초자산명']]
    end06_17_data = [row for row in kospi_200_data if '2024/06/17' in row['만기일']]
    mire_data = [row for row in kospi_200_data if '미래에셋증권' in row['LP명']]
    print(len(mire_data))
    # '코스피200'을 포함하는 항목을 만기일 기준으로 정렬
    # sorted_kospi_200_data = sorted(end06_17_data, key=lambda x: datetime.strptime(x['만기일'], '%Y/%m/%d'))
    # # 상위 30개 항목 출력
    codename = []
    for row in mire_data:
        # print(f'what name{row["종목명"]} : baseV {float(row["행사가격"])-374.8} : endV {row["최종종가"]} :: {row} ')
        codename.append(row["종목코드"])
    for i in codename:
        print(i)
