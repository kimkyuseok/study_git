# csv 파일을 가지고 원하는 데이터 가져 오는 연습
import csv
import os
from datetime import datetime
# http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201030301

folder_path = r'D:\test\chackUS\study_git\95_csv\csv'
# file_name = 'data_3910_20240614.csv'
# file_name = 'data_2826_20240617.csv'
file_name = 'data_1511_20240617.csv'
full_file_path = os.path.join(folder_path, file_name)

with open(full_file_path, 'r') as file:
    reader = csv.DictReader(file)
    data = [{k: v for k, v in row.items()} for row in reader]
    # for i in data:
    #     print(i)
    kospi_200_data = [row for row in data if 'KOSPI200콜' in row['종목명'] and row['거래량'] != '0']
    kospi_200_data_a = sorted(kospi_200_data, key=lambda x: int(x['거래량']), reverse=True)
    call = kospi_200_data_a
    kospi_200_data = [row for row in data if 'KOSPI200풋' in row['종목명'] and row['거래량'] != '0']
    kospi_200_data_b = sorted(kospi_200_data, key=lambda x: int(x['거래량']), reverse=True)
    put = kospi_200_data_b
    if kospi_200_data_b:
        for i in kospi_200_data_b[:30]:
            print(i)
        print(len(kospi_200_data_b))
    else:
        print(len(kospi_200_data_b))

    if kospi_200_data_a:
        for i in kospi_200_data_a[:30]:
            print(i)
        print(len(kospi_200_data_a))
    else:
        print(len(kospi_200_data_a))

# 거래량을 뽑아서 거래량많은순 으로 찾고 티커? 를 찾아