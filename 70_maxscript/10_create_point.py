from pymxs import runtime as rt

def create_point(name, position):
    point = rt.Point()
    point.name = name
    point.position = rt.Point3(*position)
    return point

# 사용 예시
point_name = "MyPoint"
point_position = [100, 200, 300]  # X, Y, Z 좌표
new_point = create_point(point_name, point_position)

"""
이 스크립트는 다음과 같이 작동합니다:

pymxs 모듈에서 runtime을 가져옵니다. 이를 통해 MaxScript 함수에 접근할 수 있습니다.

create_point 함수를 정의합니다. 이 함수는 이름과 위치를 매개변수로 받습니다.

함수 내에서 rt.Point()를 사용하여 새로운 Point 헬퍼를 생성합니다.

생성된 Point의 이름을 설정합니다.

rt.Point3를 사용하여 Point의 위치를 설정합니다. *position은 리스트를 언패킹하여 X, Y, Z 좌표를 개별 인자로 전달합니다.

생성된 Point 객체를 반환합니다.

사용 시에는 원하는 이름과 위치 좌표를 지정하여 함수를 호출하면 됩니다. 예를 들어, create_point("MyPoint",[100][200][300])은 (100, 200, 300) 위치에 "MyPoint"라는 이름의 Point 헬퍼를 생성합니다.

주의: 이 스크립트를 실행하려면 3ds Max의 Python 스크립트 환경에서 실행해야 합니다. 일반 Python 환경에서는 pymxs 모듈을 import할 수 없습니다.

"""
