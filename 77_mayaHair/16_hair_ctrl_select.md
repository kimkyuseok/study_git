알겠습니다. PyQt를 사용하여 처음부터 라디오 버튼과 숫자를 입력하는 UI를 만들고, 해당 UI에서 선택한 컨트롤을 마야에서 선택하는 스크립트를 작성해보겠습니다.

```python
from PySide2 import QtWidgets, QtGui
import maya.cmds as cmds

class CustomSelectToolUI(QtWidgets.QWidget):
    def __init__(self):
        super(CustomSelectToolUI, self).__init__()

        self.setWindowTitle("Custom Select Tool")
        self.setGeometry(200, 200, 300, 150)

        self.create_ui()

    def create_ui(self):
        layout = QtWidgets.QVBoxLayout()

        label = QtWidgets.QLabel("Select Control Type:")
        layout.addWidget(label)

        self.outer_radio = QtWidgets.QRadioButton("Outer")
        self.inner_radio = QtWidgets.QRadioButton("Inner")

        radio_layout = QtWidgets.QHBoxLayout()
        radio_layout.addWidget(self.outer_radio)
        radio_layout.addWidget(self.inner_radio)
        layout.addLayout(radio_layout)

        label = QtWidgets.QLabel("Enter Number:")
        layout.addWidget(label)

        self.number_spinbox = QtWidgets.QSpinBox()
        layout.addWidget(self.number_spinbox)

        select_btn = QtWidgets.QPushButton("Select")
        select_btn.clicked.connect(self.select_ctrl)
        layout.addWidget(select_btn)

        self.setLayout(layout)

    def select_ctrl(self):
        ctrl_type = "outer" if self.outer_radio.isChecked() else "inner"
        selected_number = self.number_spinbox.value()
        ctrl_name = f"kai_mermaid:{ctrl_type}{selected_number:03d}_ctrl"
        
        # 마야에서 해당 컨트롤 선택
        cmds.select(ctrl_name)

# 실행 함수
def show_custom_select_tool_ui():
    global custom_select_tool_ui
    try:
        custom_select_tool_ui.close()  # 닫힌 창이 있는 경우 먼저 닫기
    except:
        pass
    custom_select_tool_ui = CustomSelectToolUI()
    custom_select_tool_ui.show()

# 스크립트 실행
show_custom_select_tool_ui()
```

이 스크립트를 마야 스크립트 에디터나 스크립트 창에서 실행하면, UI가 나타나고 "Outer" 또는 "Inner" 라디오 버튼을 선택하고 숫자를 입력한 후 "Select" 버튼을 클릭하면 해당하는 컨트롤이 마야에서 선택됩니다.
