"""
-- Script Name: point test
-- Description: creating pos point helper   point helper  size color box  :: pointConstraint Position_Constraint test
-- Version: 1.01
-- Author: kimkyuseok
-- Date Created: 2025-02-24
-- Date Modified: 2025-02-24
-- References: https://help.autodesk.com/view/MAXDEV/2024/ENU/?guid=GUID-95453E22-A022-4543-B31C-A052CECD3598
-- Requirements: 3ds Max 2024 or later
-- Usage: Run the script from the MAXScript editor. Select the objects you want to align.
"""
import pymxs
rt = pymxs.runtime

# 헬퍼 설정
POINT_SIZE = 3
HELPER_COLOR = rt.Color(6, 153, 6)  # 녹색


def generate_unique_name(base_name):
    parts = base_name.split()
    if parts[-1].isdigit():
        # 마지막 부분이 숫자인 경우
        new_name = base_name
        counter = int(parts[-1])
        while rt.getNodeByName(new_name) is not None:
            counter += 1
            new_name = f"{' '.join(parts[:-1])} {counter}"
    else:
        # 마지막 부분이 숫자가 아닌 경우
        new_name = f"{base_name} 0"
        while rt.getNodeByName(new_name) is not None:
            counter = int(new_name.split()[-1]) + 1
            new_name = f"{base_name} {counter}"
    return new_name

def create_constrained_point(point1_name, point2_name, weight1, weight2):
    point1 = rt.getNodeByName(point1_name)
    point2 = rt.getNodeByName(point2_name)
    
    if not point1 or not point2:
        print("Error: One or both of the specified points do not exist.")
        return None
    
    new_point_name = generate_unique_name(point1_name)
    
    new_point = rt.Point()
    new_point.name = new_point_name
    new_point.size = POINT_SIZE
    new_point.wirecolor = HELPER_COLOR
    #new_point.position = (point1.position + point2.position) / 2
    
    pos_constraint = rt.Position_Constraint()
    rt.refs.replaceReference(new_point.controller, 1, pos_constraint)
    pos_constraint.appendTarget(point1, weight1)
    pos_constraint.appendTarget(point2, weight2)
    
    new_point.pos.controller = pos_constraint
    
    if point1.parent is not None:
        new_point.parent = point1.parent
    
    print(f"Created constrained point: {new_point.name}")
    return new_point

# 함수 사용 예시 Forearm
create_constrained_point("Bip001 pos L Forearm 0", "Bip001 pos L Hand 0", 67, 33)
create_constrained_point("Bip001 pos L Forearm 0", "Bip001 pos L Hand 0", 33, 67)

create_constrained_point("Bip001 pos L UpperArm 0", "Bip001 pos L Forearm 0", 67, 33)
create_constrained_point("Bip001 pos L UpperArm 0", "Bip001 pos L Forearm 0", 33, 67)
