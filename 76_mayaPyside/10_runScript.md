다음은 Pyside2를 사용하여 Maya UI를 생성하고, 특정 폴더에 있는 Python 스크립트 파일을 리스트로 표시하며, 선택된 스크립트를 실행할 수 있는 간단한 예제입니다.

```python
from PySide2 import QtWidgets, QtGui
import os

class ScriptRunnerUI(QtWidgets.QWidget):
    def __init__(self, scripts_folder, parent=None):
        super(ScriptRunnerUI, self).__init__(parent)

        self.scripts_folder = scripts_folder

        self.script_list_widget = QtWidgets.QListWidget(self)
        self.run_button = QtWidgets.QPushButton('Run Script', self)
        self.run_button.clicked.connect(self.run_selected_script)

        self.setup_ui()
        self.load_scripts()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.script_list_widget)
        layout.addWidget(self.run_button)

    def load_scripts(self):
        scripts = [f for f in os.listdir(self.scripts_folder) if f.endswith('.py')]

        for script in scripts:
            item = QtWidgets.QListWidgetItem(script)
            self.script_list_widget.addItem(item)

    def run_selected_script(self):
        selected_item = self.script_list_widget.currentItem()

        if selected_item:
            script_name = selected_item.text()
            script_path = os.path.join(self.scripts_folder, script_name)
            self.execute_script(script_path)

    def execute_script(self, script_path):
        try:
            with open(script_path, 'r') as script_file:
                script_code = script_file.read()
                exec(script_code)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Error', f"Error executing script: {str(e)}")

def show_script_runner_ui():
    scripts_folder = 'D:/work'  # 변경 필요
    app = QtWidgets.QApplication([])
    ui = ScriptRunnerUI(scripts_folder)
    ui.show()
    app.exec_()

show_script_runner_ui()
```

이 예제에서는 `D:/work` 경로에서 `.py` 확장자를 가진 스크립트 파일을 찾아 리스트로 표시하고, 선택된 스크립트를 실행할 수 있는 UI를 생성합니다. 이를 바탕으로 필요에 따라 UI를 수정하고, 스크립트를 안전하게 실행하도록 추가적인 보안 체크 등을 적용할 수 있습니다.
