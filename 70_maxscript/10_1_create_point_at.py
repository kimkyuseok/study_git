from pymxs import runtime as rt

def create_point_at(node_name, point_name):
    target_node = rt.getNodeByName(node_name)
    if target_node is not None:
        world_position = target_node.transform.translation
        point_helper = rt.Point(name=point_name)
        point_helper.position = world_position
        point_helper.parent = target_node
        rt.redrawViews()  # 뷰포트 새로고침
        print(f"{node_name} 위치에 {point_name} Point 헬퍼 생성 완료")
        return point_helper
    else:
        print(f"{node_name} 노드를 찾을 수 없습니다")
        return None

# 함수 사용 예시
create_point_at("Bip001 L Clavicle", "Clavicle_Position_Marker")
