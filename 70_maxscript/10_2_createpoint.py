"""
-- Script Name: point test
-- Description: creating pos point helper   point helper  size color box 
-- Version: 1.01
-- Author: kimkyuseok
-- Date Created: 2025-02-23
-- Date Modified: 2025-02-23
-- References: https://help.autodesk.com/view/MAXDEV/2024/ENU/?guid=MAXDEV_Python_using_pymxs_pymxs_objects_html
-- Requirements: 3ds Max 2024 or later
-- Usage: Run the script from the MAXScript editor. Select the objects you want to align.
"""

import pymxs
rt = pymxs.runtime

# 헬퍼 설정
POINT_SIZE = 3
HELPER_COLOR = rt.Color(6, 153, 6)  # 녹색
BOX_SIZE = rt.Point3(5, 5, 5)  # 박스 크기

def create_helper(bone_name):
    # 'Bip001'과 'L' 사이에 'pos'를 삽입
    parts = bone_name.split()
    new_name = f"{parts[0]} pos {' '.join(parts[1:])}"
    
    # 중복 이름 방지를 위한 숫자 추가
    base_name = f"{new_name} 0"
    counter = 0
    while rt.getNodeByName(base_name) is not None:
        counter += 1
        base_name = f"{new_name} {counter}"
    
    # Point 헬퍼 생성
    helper = rt.Point()
    helper.name = base_name
    helper.size = POINT_SIZE
    helper.wirecolor = HELPER_COLOR
    helper.size = POINT_SIZE
    
    # Point 헬퍼의 디스플레이를 Box로 변경
    helper.Box = True
    helper.cross = False
    
    
    
    # 본의 위치에 헬퍼 배치
    bone = rt.getNodeByName(bone_name)
    if bone:
        helper.transform = bone.transform
        
        # 헬퍼를 본에 링크 (에러 방지를 위해 try-except 사용)
        try:
            rt.resetxform(helper)
            helper.parent = bone
            #rt.parent(helper, bone)
        except:
            print(f"Warning: Could not parent {helper.name} to {bone_name}")
    
    return helper

# 본 이름 리스트
bone_names = [
    "Bip001 L Clavicle",
    "Bip001 L UpperArm",
    "Bip001 L Forearm",
    "Bip001 L Hand"
]

# 각 본에 대해 헬퍼 생성
for bone_name in bone_names:
    helper = create_helper(bone_name)
    print(f"Created helper: {helper.name}")
