마야에서 선택된 컨트롤러의 rotate 값을 CSV 파일로 저장하는 파이썬 스크립트를 작성해 보겠습니다. 이 스크립트는 현재 선택된 오브젝트들 중 컨트롤러에 해당하는 것들의 rotate 값을 가져와 CSV 파일로 저장합니다.

```python
import maya.cmds as cmds
import csv

def save_rotation_to_csv(file_path):
    # 현재 선택된 오브젝트들을 가져오기
    selected_objects = cmds.ls(selection=True, type="transform")
    
    if not selected_objects:
        cmds.warning("컨트롤러가 선택되지 않았습니다.")
        return
    
    # CSV 파일을 쓰기 모드로 열기
    with open(file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # CSV 파일의 헤더 작성
        csv_writer.writerow(["Controller", "RX", "RY", "RZ"])
        
        # 각 컨트롤러의 rotate 값을 CSV에 작성
        for controller in selected_objects:
            rx = cmds.getAttr(f"{controller}.rotateX")
            ry = cmds.getAttr(f"{controller}.rotateY")
            rz = cmds.getAttr(f"{controller}.rotateZ")
            
            # CSV 파일에 쓰기
            csv_writer.writerow([controller, rx, ry, rz])

    print(f"Rotate 값을 {file_path} 파일에 성공적으로 저장했습니다.")

# 스크립트를 실행할 때 파일 경로를 지정하여 호출
save_rotation_to_csv("C:/your/folder/path/rotate_values.csv")
```

주의: 스크립트를 실행하기 전에는 마야에서 컨트롤러를 선택하고 실행하여야 합니다. CSV 파일은 지정된 파일 경로에 생성되며, 파일 경로를 적절히 변경하여 사용하세요.
