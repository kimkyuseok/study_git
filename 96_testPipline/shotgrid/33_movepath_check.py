# 옥씨부인전 샷그리드 무브 패치 관련 exr 또는 mov 가아닌 경우
# 해당 경로에 mov 가 아닌 경로가 적히는 문제? 발견 대응

# ShotGrid에서 프로젝트 정보 가져오기
project = sg.find_one("Project", [["name", "is", project_name]])
print(project)

if project:
    # 프로젝트 내 모든 샷 가져오기
    # shots = sg.find("Shot", [["project", "is", project]], ["id", "code", "sg_cut_in", "sg_cut_out"])

    # 최신 200개의 main 테스크 버전 가져오기
    main_tasks_versions = sg.find("Version",
                                  [["sg_task.Task.content", "is", "main"],
                                   ["project", "is", project]],
                                  ["code", 'sg_path_to_frames', 'sg_path_to_movie'],
                                  # limit=200,
                                  order=[{"field_name": "created_at", "direction": "desc"}])

    for version in main_tasks_versions:
        if 'sg_path_to_movie' in version:
            if version['sg_path_to_movie']:
                if version['sg_path_to_movie'].find('.mov') != -1:
                    pass
                else:
                    if version['sg_path_to_frames'] != None:
                        print(version)
                        sg.update("Version", int(version['id']), {"sg_path_to_movie": ''})