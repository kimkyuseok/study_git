마야(Maya)에서 PyQt를 사용하여 사용자 정의 UI를 만들어보겠습니다. 아래는 PyQt를 사용한 간단한 예제 코드입니다.

```python
from PySide2 import QtWidgets, QtGui, QtCore
import maya.cmds as cmds

class CustomSelectToolUI(QtWidgets.QWidget):
    def __init__(self):
        super(CustomSelectToolUI, self).__init__()

        self.setWindowTitle("Custom Select Tool")
        self.setGeometry(200, 200, 300, 100)

        self.create_ui()

    def create_ui(self):
        layout = QtWidgets.QVBoxLayout()

        label = QtWidgets.QLabel("Select Control:")
        layout.addWidget(label)

        outer_ctrl_btn = QtWidgets.QPushButton("outer_ctrl")
        outer_ctrl_btn.clicked.connect(lambda: self.select_ctrl("outer"))
        layout.addWidget(outer_ctrl_btn)

        inner_ctrl_btn = QtWidgets.QPushButton("inner_ctrl")
        inner_ctrl_btn.clicked.connect(lambda: self.select_ctrl("inner"))
        layout.addWidget(inner_ctrl_btn)

        self.setLayout(layout)

    def select_ctrl(self, ctrl_type):
        selected_number, ok = QtWidgets.QInputDialog.getInt(self, "Enter Number", "Enter a number:")
        if ok:
            ctrl_name = f"kai_mermaid:{ctrl_type}{selected_number:03d}_ctrl"
            cmds.select(ctrl_name)

def show_custom_select_tool_ui():
    global custom_select_tool_ui
    try:
        custom_select_tool_ui.close()  # 닫힌 창이 있는 경우 먼저 닫기
    except:
        pass
    custom_select_tool_ui = CustomSelectToolUI()
    custom_select_tool_ui.show()

show_custom_select_tool_ui()
```

이 코드는 PyQt를 사용하여 간단한 UI를 만들고, "outer_ctrl" 및 "inner_ctrl" 버튼을 클릭하면 해당하는 컨트롤을 선택하도록 하는 예제입니다. 사용자에게 숫자를 입력받아서 해당하는 숫자를 컨트롤 이름에 적용하게끔 했습니다.

이 코드를 마야 스크립트 에디터나 스크립트 창에서 실행하면 UI가 나타나고, "outer_ctrl" 또는 "inner_ctrl" 버튼을 클릭하여 선택할 수 있습니다.
