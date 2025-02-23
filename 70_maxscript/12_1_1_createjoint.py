"""
-- Script Name: create joint bon
-- Description: create point 1 point2 joint
-- Version: 1.01
-- Author: kimkyuseok
-- Date Created: 2025-02-24
-- Date Modified: 2025-02-24
-- References: https://help.autodesk.com/view/MAXDEV/2024/ENU/?guid=GUID-6BD7F514-04E9-45E9-A10D-D63E837074C6
-- Requirements: 3ds Max 2024 or later
-- Usage: Run the script from the MAXScript editor. Select the objects you want to align.
"""
import pymxs
rt = pymxs.runtime

def create_bone_chain(point_helper_names):
    if len(point_helper_names) < 2:
        print("Error: At least two point helpers are required to create a bone.")
        return

    # 본 시스템 초기화
    rt.BoneSys.createBoneChainMode = False  # 단일 본 생성 모드

    bones = []
    for i in range(len(point_helper_names) - 1):
        start_point_helper = rt.getNodeByName(point_helper_names[i])
        end_point_helper = rt.getNodeByName(point_helper_names[i+1])

        if start_point_helper is None or end_point_helper is None:
            print(f"Error: Point helper '{point_helper_names[i]}' or '{point_helper_names[i+1]}' not found.")
            continue

        # 본 생성
        bone = rt.BoneSys.createBone(
            start_point_helper.transform.translation,  # 시작 지점
            end_point_helper.transform.translation,    # 종료 지점
            rt.Point3(0, 1, 0),        
        )

        # 본 속성 설정
        bone.width = 1.0    # 본 두께
        bone.height = 1.0   # 본 높이
        bone.name = f"Bone_{i+1}" # 본 이름

        # 본 핀 설정 (시각화 용이)
        bone.frontFin = 2.0  # 전방 핀 크기
        bone.sideFins = True  # 측면 핀 활성화

        bones.append(bone)

    # 화면 갱신
    rt.redrawViews()

    return bones
    
def parent_bones_in_chain(bone_list, new_bonename_list=None):
    if len(bone_list) < 2:
        print("Error: At least two bones are required to create a hierarchy.")
        return

    # 새 이름 리스트가 제공되었고, 본 리스트와 길이가 다르면 오류 메시지 출력
    if new_bonename_list and len(new_bonename_list) != len(bone_list):
        print("Error: The length of new_bonename_list does not match the length of bone_list.")
        return

    for i in range(len(bone_list)):
        if i < len(bone_list) - 1:
            child_bone = bone_list[i + 1]
            parent_bone = bone_list[i]
            
            # 자식 본의 부모를 설정
            child_bone.parent = parent_bone

        # 새 이름 리스트가 제공된 경우, 본의 이름 변경
        if new_bonename_list:
            bone_list[i].name = new_bonename_list[i]

    print("Bone hierarchy created successfully.")
    if new_bonename_list:
        print("Bone names updated successfully.")
    

# 사용 예시:
point_list = [
    "Bip001 pos L Forearm 0",
    "Bip001 pos L Forearm 1",
    "Bip001 pos L Forearm 2",
    "Bip001 pos L Hand 0"
]


created_bones = create_bone_chain(point_list)

newbonname_list = [
    "Bip001 jnt L Forearm 0",
    "Bip001 jnt L Forearm 1",
    "Bip001 jnt L Forearm 2"    
]
# 생성된 본들을 계층 구조로 설정
parent_bones_in_chain(created_bones,newbonname_list)
