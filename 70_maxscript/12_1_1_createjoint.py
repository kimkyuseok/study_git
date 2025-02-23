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

# 사용 예시:
point_list = [
    "Bip001 pos L Forearm 0",
    "Bip001 pos L Forearm 1",
    "Bip001 pos L Forearm 2",
    "Bip001 pos L Hand 0"
]

created_bones = create_bone_chain(point_list)
