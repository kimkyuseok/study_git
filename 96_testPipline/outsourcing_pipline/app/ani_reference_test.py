# 외주사 쥐 레퍼런스 교체 스크립트
# 애니 씬 파일 레퍼런스 교체
import maya.cmds as cmds
def get_reference_list():
    # 현재 열려 있는 씬에서 레퍼런스 리스트 가져오기
    reference_list = cmds.ls(references=True)
    # 레퍼런스 이름과 파일 경로를 담을 딕셔너리
    reference_info = {}
    for ref_node in reference_list:
        # 레퍼런스 노드로부터 파일 경로 가져오기
        file_path = cmds.referenceQuery(ref_node, filename=True)
        # 딕셔너리에 레퍼런스 이름과 파일 경로 저장
        reference_info[ref_node] = file_path
    return reference_info

def replace_reference(reference_name, new_path):
    try:
        # 레퍼런스 이름에서 필요한 값 추출 (예: 'rat_rig_v01RN'에서 'rat' 추출)
        ref_key = reference_name.split('_rig')[0]
        # 데이터로 제공된 경로로 레퍼런스 교체
        cmds.file(new_path, loadReference=reference_name, type="mayaBinary", options="v=0")
        # 교체 성공 메시지 출력
        print(f"Successfully replaced reference '{reference_name}' with path '{new_path}' for key '{ref_key}'.")
    except Exception as e:
        print(f"Failed to replace reference '{reference_name}' with path '{new_path}': {str(e)}")


result = get_reference_list()
# 데이터 딕셔너리
data = {'rat': 'X:/VFX/moe/asset/character/rat/rig/pub/scenes/rat_rig.mb'}
# 각 레퍼런스에 대해 교체 작업 실행
for ref_name, new_file_path in data.items():
    for current_ref_name, current_file_path in result.items():  # result는 이전에 얻은 레퍼런스 정보 딕셔너리입니다.
        if ref_name == current_ref_name.split('_rig')[0]:
            replace_reference(current_ref_name, new_file_path)