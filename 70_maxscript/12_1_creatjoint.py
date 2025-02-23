import pymxs
rt = pymxs.runtime

# 포인트 생성
point1 = rt.Point(name="Start_Point")
point2 = rt.Point(name="End_Point")

# 포인트 위치 설정 (X축으로 100단위 간격)
point1.pos = rt.Point3(0, 0, 0)
point2.pos = rt.Point3(10, 0, 0)

# 본 시스템 초기화
rt.BoneSys.createBoneChainMode = False  # 단일 본 생성 모드

# 본 생성
bone = rt.BoneSys.createBone(
    point1.pos,  # 시작 지점
    point2.pos,  # 종료 지점
    rt.Point3(0, 1, 0),        
)

# 본 속성 설정
bone.width = 5.0    # 본 두께
bone.height = 5.0   # 본 높이
bone.name = "MyBone" # 본 이름

# 본 핀 설정 (시각화 용이)
#rt.setBoneFins(bone, rt.Name('all'), True)  # 모든 핀 활성화
bone.frontFin = 10.0  # 전방 핀 크기
bone.sideFins = True  # 측면 핀 활성화

# 화면 갱신
rt.redrawViews()
