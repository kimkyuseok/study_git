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
list_version_edit=[]
returnVersion=[]
# 'edit' 태스크가 포함된 버전만 필터링
for version in versions:
    if version['sg_task']:
        if version['sg_task']['name'] == 'edit':
            returnVersion.append(version)
# 필터링된 버전 중 마지막 6개만 출력
for version in returnVersion[:250]:
    #print(f"Version Code: {version['id']} : {version['code']} :  {version['created_at']}")
    #print(f"https://vive.shotgunstudio.com/detail/Shot/30948#Version_{version['id']}")
    list_version_edit.append(version['id'])
#print(list_version_edit)
# 여기에 마지막으로 작업한  이벤트 번호를 적고!
last_event_file_path = r'T:\TD\in\dxp_plate_plus1000\his\last_edit_event_number.txt'
last_event = 152753 # 예를 들어 152557 이라하면 앞에 한개가 더 있어야해.

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


num=0
endnum=0
for i in list_version_edit:
    if int(i) == int(last_event):
        endnum=num
    num = num+1

version_in_list = []
if endnum != 0:
    version_in_list = list_version_edit[:endnum]
    # 저장할 특정 단어
    specific_word = list_version_edit[0]
    # 오늘 날짜를 'YYYYMMDD' 형식으로 얻기
    today_date = datetime.now().strftime('%Y%m%d')
    # 새 파일 이름 생성
    new_file_name = f'his_last_edit_event_number_{today_date}.txt'
    new_file_path = os.path.join(os.path.dirname(last_event_file_path), new_file_name)
    try:
        # 특정 단어를 파일에 작성
        with open(last_event_file_path, 'w') as file:
            file.write(specific_word)
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
else:
    print(f'최신 50개에 없음 {endnum} {list_version_edit}' )




for version_id_num in version_in_list:
    version_id = version_id_num
    print(f"https://vive.shotgunstudio.com/detail/Shot/30948#Version_{version_id}")
    fields_to_fetch = ['code', 'sg_path_to_frames', 'sg_path_to_movie', 'sg_task', 'frame_range']  # 원하는 필드를 명시합니다.
    # 필터 조건을 올바르게 설정합니다.
    filters = [['id', 'is', version_id]]
    # find 메서드를 호출하여 결과를 가져옵니다.
    versions_a = sg.find("Version", filters, fields_to_fetch)
    shot_name = versions_a[0]['code'].split('_edit')[0]
    print(version_id, shot_name)
    shot = sg.find_one("Shot",
                       [["project", "is", {"type": "Project", "id": project_id}], ["code", "is", shot_name]],
                       ["id","sg_cut_in","sg_cut_out",'sg_versions'])
    if shot==None:
        shot = sg.find_one("Shot",
                           [["project", "is", {"type": "Project", "id": project_id}], ["code", "is", shot_name[:-4]+'c'+shot_name[-4:]]],
                           ["id", "sg_cut_in", "sg_cut_out", 'sg_versions'])
    version_main_list=[]
    # main task에 sg_path_to_frames mov가 있을경우 삭제가 필요해보임
    print(version_id, shot)
    if shot['sg_versions']:
        for i in shot['sg_versions']:
            if i['name'].find('_main_')!=-1:
                version_a = sg.find_one("Version", [["id", "is", i['id']]], ["code", "sg_path_to_frames", "sg_path_to_movie"])
                version_main_list.append(version_a)
                if version_a['sg_path_to_frames']:
                    # dpx인데 mov 이면 에러
                    if (version_a['sg_path_to_frames'][-4:]) == '.mov':
                        print('remove sg_path_to_frames mov')
                        sg.update("Version", version_a['id'], {"sg_path_to_frames": None})
                if version_a['sg_path_to_movie']:
                    if (version_a['sg_path_to_movie'][-4:]) == '.dpx':
                        print('remove sg_path_to_movie dpx')
                        sg.update("Version", version_a['id'], {"sg_path_to_movie": None})
    print(shot)
    print(versions_a)
    print(len(version_main_list))
    # 경우의수 sg_path_to_frames 에 dpx가 있을경우
    # print(versions_a[0]['sg_path_to_frames'])
    if versions_a[0]['sg_path_to_frames']:
        # dpx 자리에 mov일 경우
        if (versions_a[0]['sg_path_to_frames'][-4:]) == '.mov':
            s_mov = versions_a[0]['sg_path_to_frames'][-4:]
            if versions_a[0]['sg_path_to_movie'] == None:
                print(f" none move") # mov 자리가 비었을 경우
                cut_in_a = shot['sg_cut_in']
                cut_out_a = shot['sg_cut_out']
                if int(cut_in_a) > 1000:
                    cut_in_a = str(int(cut_in_a)-1000)
                if int(cut_out_a) > 1000:
                    cut_out_a = str(int(cut_out_a)-1000)
                sg.update("Version", version_id, {"sg_path_to_frames": None,
                                                  "sg_path_to_movie": versions_a[0]['sg_path_to_frames'],
                                                  "frame_range": f'{cut_in_a}-{cut_out_a}'})
        elif (versions_a[0]['sg_path_to_frames'][-4:]) == '.dpx':
            check = check_dpx_files(versions_a[0]['sg_path_to_frames'])
            print(f'dpx : {check}')
            if check == False:
                sg.update("Version", version_id, {"sg_path_to_frames": None})
        else:
            pass
    if versions_a[0]['sg_path_to_movie']:
        if (versions_a[0]['sg_path_to_movie'][-4:]) == '.mov':
            """
            cut_in_a = shot['sg_cut_in']
            cut_out_a = shot['sg_cut_out']
            if int(cut_in_a) > 1000:
                cut_in_a = str(int(cut_in_a) - 1000)
            if int(cut_out_a) > 1000:
                cut_out_a = str(int(cut_out_a) - 1000)
            """
            if versions_a[0]['frame_range']:
                inout=versions_a[0]['frame_range'].split('-')
                cut_in_a = inout[0]
                cut_out_a = inout[1]
                if int(cut_in_a) > 1000:
                    cut_in_a = str(int(cut_in_a) - 1000)
                if int(cut_out_a) > 1000:
                    cut_out_a = str(int(cut_out_a) - 1000)
                if versions_a[0]['frame_range'] == f'{cut_in_a}-{cut_out_a}':
                    print('pass')
                else:
                    print(f'check {versions_a[0]["frame_range"]} :: {cut_in_a}-{cut_out_a} ')
                    sg.update("Version", version_id, {"frame_range": f'{cut_in_a}-{cut_out_a}'})

    # version_main_list 중에 최신버전찾기
    if version_main_list:
        last_version_main = None
        for i in version_main_list:
            #print(i)
            if last_version_main == None:
                last_version_main = i
            else:
                if last_version_main['code'].find('_main_v')!=-1:
                    num=last_version_main['code'].split('_main_v')
                    inum=i['code'].split('_main_v')
                    if int(inum[1]) > int(num[1]):
                        last_version_main = i
        # 메인 마지막 버전에 dpx가 있으면
        if last_version_main['sg_path_to_frames']:
            if last_version_main['sg_path_to_frames'][-4:] == '.dpx':
                # 수정된 버전 다시 가져오기
                versions_b = sg.find("Version", filters, fields_to_fetch)
                # edit frame range + 1000
                if versions_b[0]['frame_range']:
                    inout = versions_b[0]['frame_range'].split('-')
                    cut_in_a = str(int(inout[0])+1000)
                    cut_out_a = str(int(inout[1])+1000)
                    cut_in_b = shot['sg_cut_in']
                    cut_out_b = shot['sg_cut_out']
                    print(f'check shot: {cut_in_b}-{cut_out_b} :  edit: {cut_in_a}-{cut_out_a} ')
                    if not {cut_in_b}-{cut_out_b} == {cut_in_a}-{cut_out_a}:
                        sg.update("Shot", shot['id'], {"sg_cut_in": int(cut_in_a) , "sg_cut_out": int(cut_out_a) })

        versions_c = sg.find("Version", filters, fields_to_fetch)
        if versions_c[0]['frame_range']==None:
            print(f'===============================error================frame_range=====>>>>>>>{version_id}')