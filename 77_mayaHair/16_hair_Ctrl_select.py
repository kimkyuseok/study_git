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

        label = QtWidgets.QLabel("Select Control Type:")
        layout.addWidget(label)

        self.A_radio = QtWidgets.QRadioButton("A")
        self.B_radio = QtWidgets.QRadioButton("B")
        self.C_radio = QtWidgets.QRadioButton("C")
        self.D_radio = QtWidgets.QRadioButton("D")
        self.E_radio = QtWidgets.QRadioButton("E")
        self.F_radio = QtWidgets.QRadioButton("F")
        self.G_radio = QtWidgets.QRadioButton("G")
        self.H_radio = QtWidgets.QRadioButton("H")                        

        radio1_layout = QtWidgets.QHBoxLayout()
        radio1_layout.addWidget(self.A_radio)
        radio1_layout.addWidget(self.B_radio)
        radio1_layout.addWidget(self.C_radio)
        radio1_layout.addWidget(self.D_radio)
        radio1_layout.addWidget(self.E_radio)
        radio1_layout.addWidget(self.F_radio)
        radio1_layout.addWidget(self.G_radio)
        radio1_layout.addWidget(self.H_radio)                        
        layout.addLayout(radio1_layout)
        

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
        ctrl_name = f"kai_mermaid:{ctrl_type}{selected_number:03d}A_ctrl"
        
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
