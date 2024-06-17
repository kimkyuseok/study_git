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
    sorted_data = sorted(data, key=lambda x: datetime.strptime(x['만기일'], '%Y/%m/%d'))
    # 상위 두 개의 행 출력
    for row in sorted_data[:2]:
        print(row)
