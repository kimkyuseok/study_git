# 여러개의 스킨 폴리곤과  컴파인된  폴리곤을 주면 ( 조인트가 같다는 전제하에 ) 스킨카피를 해준다.

# 모듈 임포트
import maya.cmds as cmds
import maya.mel as mel

# 함수 생성 poly_copy   변수  폴리곤 2개주면 a->b 가까운 버텍스 스킨 카피
def poly_copy(polygonA,polygonB):
    # 각각 버텍스 찾기
    verticesA = cmds.ls(polygonA + '.vtx[*]', flatten=True)
    verticesB = cmds.ls(polygonB + '.vtx[*]', flatten=True)
    vertexcopylist=[]
    # a 버텍스 기준으로 for문
    for i in verticesA:
        # a 폴리곤 버텍스 i번째 위치 알아내기
        v_position = cmds.xform(i, query=True, translation=True, worldSpace=True)
        # 최단거리 버텍스  값을 받을 빈공간 생성
        closest_vertex = None
        # 최소 거리값 받을 빈공간 생성
        min_distance = float('inf')
        # b 버텍스 기준으로 for 문
        for vertex in verticesB:
            # b 폴리곤 버텍스 i번째 위치 알아내기
            vertex_position = cmds.xform(vertex, query=True, translation=True, worldSpace=True)
            # 거리값 알아내기
            distance = sum((a - b) ** 2 for a, b in zip(v_position, vertex_position)) ** 0.5
            # 최소값 거리이면
            if distance < min_distance:
                # 최소값 거리 갱신
                min_distance = distance
                # 최단거리 버텍스 갱신
                closest_vertex = vertex
        #print (i,closest_vertex)
        vertexcopylist.append(closest_vertex)
    # 폴리곤 a  버텍스 리스트 카피
    cmds.select(polygonA,vertexcopylist)
    mel.eval('copySkinWeights  -noMirror -surfaceAssociation closestPoint -influenceAssociation oneToOne -influenceAssociation oneToOne -influenceAssociation oneToOne;')

selObj = cmds.ls(sl=1)
polygonB = selObj[-1]
for i in selObj:
    if i!= polygonB:
        poly_copy(i,polygonB)