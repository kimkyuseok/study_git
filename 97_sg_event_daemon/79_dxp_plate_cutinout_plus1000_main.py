# 특정버전-main-을 주면 path to frame , path to movie 검사해서 정상처리한다.
import sys
sys.version
scriptPath=r'T:/inhouse/pub/maya/lib'
sys.path.append(scriptPath)
import shutil
from datetime import datetime
import os
import glob
import shotgun_api3
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from base64 import urlsafe_b64encode, urlsafe_b64decode
from cryptography.hazmat.backends import default_backend
import os
import pickle
import ast

scriptname='vive_sg_daemon'
in_house_data = r't:/inhouse-data/sg_script_set/script.dat'
encrypted_data = None
with open(in_house_data, 'rb') as file:
    content = pickle.load(file)
    #print(content)
    encrypted_data = content[scriptname]
if encrypted_data:
    with open(r't:/TD/data/shotgrid.dat', 'r') as file:
        sgitem = file.read()
        #print(sgitem)
    sgitem_dict = ast.literal_eval(sgitem)
    key = hashlib.pbkdf2_hmac(sgitem_dict['hash_name'], sgitem_dict['password'].encode(), sgitem_dict['salt'].encode(), 100000)
    iv = b'\x00' * 16
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(urlsafe_b64decode(encrypted_data)) + decryptor.finalize()
    #print(decrypted_data.decode())
# dpx 파일이 없으면
def check_dpx_files(directory_pattern):
    # Generate the pattern for .dpx files
    dpx_pattern = directory_pattern.replace('%04d', '*')
    # Search for .dpx files matching the pattern
    dpx_files = glob.glob(dpx_pattern)
    if dpx_files:
        print(f"Found {len(dpx_files)} .dpx file(s).")
        for file in dpx_files:
            print(f"File found: {file}")
        return True
    else:
        print("No .dpx files found.")
        return False
class TestShotgrid(shotgun_api3.Shotgun):
    URL = sgitem_dict['url']
    SCRIPT_NAME = scriptname
    SCRIPT_KEY = decrypted_data.decode()
    # 내부망 접속
    PROXY_IP = sgitem_dict['ip']
    # 내부망 접속 포트
    PROXY_PORT = sgitem_dict['port']
    def __init__(self):
        super(TestShotgrid, self).__init__(self.URL, self.SCRIPT_NAME, self.SCRIPT_KEY,
        http_proxy=f'{self.PROXY_IP}:{self.PROXY_PORT}')

sg = TestShotgrid()
project_name='moe'
project = sg.find_one("Project", [["name", "is", project_name]], ["id"])
project_id=None
if project:
    project_id = project["id"]

project = sg.find_one("Project", [["name", "is", project_name]])
# 프로젝트 내 모든 샷 가져오기
Versions = sg.find("Version", [["project", "is", project]], ["id", "code"])
# 프로젝트 검색
project = sg.find_one("Project", [["name", "is", project_name]])
if not project:
    print(f"Project '{project_name}' not found.")
    exit()

# 프로젝트 내 모든 버전 검색
versions = sg.find("Version", [["project", "is", project]], ["id", "code", "sg_task",'created_at'],order=[{'field_name': 'created_at', 'direction': 'desc'}])
print(f"Total versions found: {len(versions)}")
list_version_main=[]
returnVersion=[]
# 'edit' 태스크가 포함된 버전만 필터링
for version in versions:
    if version['sg_task']:
        if version['sg_task']['name'] == 'main':
            returnVersion.append(version)
# 필터링된 버전 중 마지막 6개만 출력
for version in returnVersion[:250]:
    # print(f"Version Code: {version['id']} : {version['code']} :  {version['created_at']}")
    # print(f"https://vive.shotgunstudio.com/detail/Shot/30948#Version_{version['id']}")
    list_version_main.append(version['id'])

#print(list_version_edit)
# 여기에 마지막으로 작업한  이벤트 번호를 적고!
last_event_file_path = r'T:\TD\in\dxp_plate_plus1000\his\last_main_event_number.txt'
#last_event = 152753 # 예를 들어 152557 이라하면 앞에 한개가 더 있어야해.

# 파일 읽기 및 첫 번째 줄의 첫 번째 단어 출력
try:
    with open(last_event_file_path, 'r') as file:
        # 첫 번째 줄 읽기
        first_line = file.readline().strip()
        # 첫 번째 줄의 첫 번째 단어 추출
        first_word = first_line.split()[0]
        print(f"첫 번째 단어: {first_word}")
        last_event=first_word
except FileNotFoundError:
    print(f"파일을 찾을 수 없습니다: {last_event_file_path}")
except IndexError:
    print("파일의 첫 번째 줄에 단어가 없습니다.")
except Exception as e:
    print(f"오류가 발생했습니다: {e}")

print(last_event,list_version_main)
num=0
endnum=0
for i in list_version_main:
    if int(i) == int(last_event):
        endnum=num
    num = num+1

version_in_list = []
if endnum != 0:
    version_in_list = list_version_main[:endnum]
    # 저장할 특정 단어
    specific_word = list_version_main[0]
    # 오늘 날짜를 'YYYYMMDD' 형식으로 얻기
    today_date = datetime.now().strftime('%Y%m%d')
    # 새 파일 이름 생성
    new_file_name = f'his_last_main_event_number_{today_date}.txt'
    new_file_path = os.path.join(os.path.dirname(last_event_file_path), new_file_name)
    print(f' 저장해야할꺼{specific_word}')
    try:
        # 특정 단어를 파일에 작성
        with open(last_event_file_path, 'w') as file:
            file.write(str(specific_word))
        print(f"파일에 '{specific_word}'이(가) 성공적으로 저장되었습니다.")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")

    try:
        # 파일 복사
        shutil.copy2(last_event_file_path, new_file_path)
        print(f"파일이 성공적으로 복사되었습니다: {new_file_path}")
    except FileNotFoundError:
        print(f"원본 파일을 찾을 수 없습니다: {last_event_file_path}")
    except PermissionError:
        print("파일에 접근할 권한이 없습니다.")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
    print(f'최신 250개에 있음 {endnum} {last_event}{list_version_main}')
else:
    print(f'최신 50개에 없음 {endnum} {last_event}{list_version_main}' )
returnPrintString=[]
returnPrintString.append(f'===========프레임레인지가 서로 다름=================')
returnPrintStringdxp=[]
returnPrintStringdxp.append(f'===========path to frames  dpx 가 아닌경우 =================')
returnPrintStringmov=[]
returnPrintStringmov.append(f'===========path to frames  mov 가 아닌경우 =================')
for version_id_num in version_in_list:
    version_id = version_id_num
    print(f"https://vive.shotgunstudio.com/detail/Shot/30948#Version_{version_id}")
    fields_to_fetch = ['code', 'sg_path_to_frames', 'sg_path_to_movie', 'sg_task', 'frame_range']  # 원하는 필드를 명시합니다.
    # 필터 조건을 올바르게 설정합니다.
    filters = [['id', 'is', version_id]]
    # find 메서드를 호출하여 결과를 가져옵니다.
    versions_a = sg.find("Version", filters, fields_to_fetch)
    shot_name = versions_a[0]['code'].split('_main')[0]
    print(version_id, shot_name)
    shot = sg.find_one("Shot",
                       [["project", "is", {"type": "Project", "id": project_id}], ["code", "is", shot_name]],
                       ["id","sg_cut_in","sg_cut_out",'sg_versions'])
    if shot==None:
        shot = sg.find_one("Shot",
                           [["project", "is", {"type": "Project", "id": project_id}], ["code", "is", shot_name[:-4]+'c'+shot_name[-4:]]],
                           ["id", "sg_cut_in", "sg_cut_out", 'sg_versions'])
    # main 기준으로 봤을때 이상할거같은거 프린트
    # main 과 shot 컷인 컷아웃이 서로 다른거 프린트
    print(f'{versions_a[0]["frame_range"]} 샷:{shot["sg_cut_in"]}-{shot["sg_cut_out"]}')

    if versions_a[0]['frame_range'] != f'{shot["sg_cut_in"]}-{shot["sg_cut_out"]}':
        returnPrintString.append(f'메인-샷 프레임레인지 가 다름 확인필요 메인:{versions_a[0]["frame_range"]} 샷:{shot["sg_cut_in"]}-{shot["sg_cut_out"]}')
        returnPrintString.append(f"https://vive.shotgunstudio.com/detail/Shot/30948#Version_{version_id}")
    # dpx 가 아닐경우 None 처리
    if versions_a[0]['sg_path_to_frames']:
        if versions_a[0]['sg_path_to_frames'][-4:] != ".dpx":
            returnPrintStringdxp.append(f'pdx 확인필요 :{versions_a[0]["sg_path_to_frames"]}')
            returnPrintStringdxp.append(f"https://vive.shotgunstudio.com/detail/Shot/30948#Version_{version_id}")
            sg.update("Version", versions_a[0]['id'], {"sg_path_to_frames": None})
    # mov 가 아닐경우 None 처리
    if versions_a[0]['sg_path_to_movie']:
        if versions_a[0]['sg_path_to_movie'][-4:] != ".mov":
            returnPrintStringdxp.append(f'mov 확인필요 :{versions_a[0]["sg_path_to_movie"]}')
            returnPrintStringdxp.append(f"https://vive.shotgunstudio.com/detail/Shot/30948#Version_{version_id}")
            sg.update("Version", versions_a[0]['id'], {"sg_path_to_movie": None})
    # 최신 edit를 구해보자.

# 최종결과 프린트
for i in returnPrintString:
    print(i)
for i in returnPrintStringdxp:
    print(i)
for i in returnPrintStringmov:
    print(i)


