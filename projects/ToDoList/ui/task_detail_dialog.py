from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QDialogButtonBox

class TaskDetailDialog(QDialog):
    def __init__(self, task, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Task Details")
        self.task = task

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Title: {task['title']}"))
        layout.addWidget(QLabel(f"Time: {task['start']} - {task['end']}"))
        layout.addWidget(QLabel(f"Tag: {task['tag']}"))

        self.description_input = QTextEdit()
        self.description_input.setText(task.get("description", ""))
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.description_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_description(self):
        return self.description_input.toPlainText().strip()
