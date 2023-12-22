import maya.cmds as cmds

def find_closest_vertex(locator, polygon):
    # 로케이터의 위치 가져오기
    loc_position = cmds.xform(locator, query=True, translation=True, worldSpace=True)

    # 폴리곤의 버텍스 가져오기
    vertices = cmds.ls(polygon + '.vtx[*]', flatten=True)

    # 가장 가까운 버텍스 찾기
    closest_vertex = None
    min_distance = float('inf')

    for vertex in vertices:
        vertex_position = cmds.xform(vertex, query=True, translation=True, worldSpace=True)
        distance = sum((a - b) ** 2 for a, b in zip(loc_position, vertex_position)) ** 0.5

        if distance < min_distance:
            min_distance = distance
            closest_vertex = vertex

    return closest_vertex

# 테스트
locator_name = 'locator1'  # 로케이터의 이름을 여기에 넣으세요
polygon_name = 'pCube1'    # 폴리곤의 이름을 여기에 넣으세요

result = find_closest_vertex(locator_name, polygon_name)
print(f"The closest vertex to the locator is: {result}")