import os


def remove_prefix_from_filenames(directory):
    # 지정한 디렉토리에서 파일 목록을 가져옴
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            old_filepath = os.path.join(directory, filename)
            # "00000-" 부분을 삭제한 새 파일 이름 생성
            fastfilename = filename.split('-',1)[0]
            new_filename = filename.replace(f"{fastfilename}-", "")
            new_filepath = os.path.join(directory, new_filename)

            # 파일 이름 변경
            os.rename(old_filepath, new_filepath)
            print(f"{filename} 파일의 이름을 {new_filename}으로 변경했습니다.")


# 함수 호출
directory_path = r'X:\VFX\sgn\shot\JJW_BS_001\stablediffusion\out'


remove_prefix_from_filenames(directory_path)