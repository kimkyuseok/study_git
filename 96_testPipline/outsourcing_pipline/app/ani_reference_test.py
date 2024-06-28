import maya.cmds as cmds

def get_reference_info():
    # 현재 씬에서 사용된 모든 레퍼런스 가져오기
    reference_nodes = cmds.ls(type='reference')

    reference_info = {}

    for ref_node in reference_nodes:
        # 레퍼런스 노드로부터 네임스페이스 가져오기
        namespace = cmds.referenceQuery(ref_node, namespace=True)
        # 레퍼런스 파일 경로 가져오기
        file_path = cmds.referenceQuery(ref_node, filename=True)

        # 딕셔너리에 네임스페이스와 파일 경로 추가
        reference_info[namespace] = file_path

    return reference_info

# 스크립트 실행 및 결과 출력
result = get_reference_info()
print(result)