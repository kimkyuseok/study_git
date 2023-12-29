from PySide2 import QtWidgets, QtGui, QtCore
import os
import traceback
from maya.app.general import mayaMixin


class ScriptRunnerUI(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QWidget):
    def __init__(self, scripts_folder, parent=None):
        super(ScriptRunnerUI, self).__init__(parent)

        self.scripts_folder = scripts_folder

        self.script_list_widget = QtWidgets.QListWidget(self)
        self.run_button = QtWidgets.QPushButton('Run Script', self)
        self.run_button.clicked.connect(self.run_all_scripts)

        self.setup_ui()
        self.load_scripts()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.script_list_widget)
        layout.addWidget(self.run_button)

        # 오른쪽 마우스 메뉴를 만들어 각 줄을 실행할 수 있게 함
        self.script_list_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.script_list_widget.customContextMenuRequested.connect(self.show_context_menu)
        self.context_menu = QtWidgets.QMenu(self.script_list_widget)
        self.run_line_action = self.context_menu.addAction('Run this line')
        self.run_line_action.triggered.connect(self.run_selected_line)

    def load_scripts(self):
        scripts = [f for f in os.listdir(self.scripts_folder) if f.endswith('.py')]

        for script in scripts:
            item = QtWidgets.QListWidgetItem(script)
            self.script_list_widget.addItem(item)

    def run_all_scripts(self):
        for row in range(self.script_list_widget.count()):
            item = self.script_list_widget.item(row)
            self.script_list_widget.setCurrentItem(item)
            self.run_selected_script()

    def run_selected_script(self):
        selected_item = self.script_list_widget.currentItem()

        if selected_item:
            script_name = selected_item.text()
            script_path = os.path.join(self.scripts_folder, script_name)
            self.execute_script(script_path)

    def execute_script(self, script_path):
        try:
            with open(script_path, 'r') as script_file:
                script_lines = script_file.readlines()

            for line in script_lines:
                self.execute_line(line)

            # 실행이 완료되면 녹색으로 표시
            selected_item = self.script_list_widget.currentItem()
            selected_item.setForeground(QtGui.QColor('green'))

        except Exception as e:
            # 오류 발생 시 빨간색으로 표시
            selected_item = self.script_list_widget.currentItem()
            selected_item.setForeground(QtGui.QColor('red'))

            traceback.print_exc()

            QtWidgets.QMessageBox.critical(self, 'Error', f"Error executing script: {str(e)}")

    def execute_line(self, line):
        try:
            exec(line)
        except Exception as e:
            traceback.print_exc()
            raise e

    def show_context_menu(self, pos):
        self.context_menu.exec_(self.script_list_widget.mapToGlobal(pos))

    def run_selected_line(self):
        selected_item = self.script_list_widget.currentItem()

        if selected_item:
            script_name = selected_item.text()
            script_path = os.path.join(self.scripts_folder, script_name)

            # 선택한 줄의 스크립트를 실행
            selected_line = selected_item.text()
            self.execute_line(selected_line)


if __name__ == '__main__':
    scripts_folder = 'D:/work/script/python_api'  # 변경 필요
    ui = ScriptRunnerUI(scripts_folder)
    ui.show()
