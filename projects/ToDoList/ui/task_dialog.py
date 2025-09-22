from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, QComboBox, QCheckBox, QTextEdit, QDateEdit
from PyQt5.QtCore import QDate

class TaskDialog(QDialog):
    def __init__(self, task_manager, selected_date):
        super().__init__()
        self.task_manager = task_manager
        self.setWindowTitle("Add Task")
        self.selected_date = selected_date
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        layout.addWidget(QLabel("Title:"))
        layout.addWidget(self.title_input)

        self.description_input = QTextEdit()
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.description_input)

        self.tag_input = QLineEdit()
        layout.addWidget(QLabel("Tag:"))
        layout.addWidget(self.tag_input)

        self.repeat_checkbox = QCheckBox("Repeat Weekly")
        layout.addWidget(self.repeat_checkbox)

        self.date_picker = QDateEdit(self.selected_date)
        self.date_picker.setCalendarPopup(True)
        layout.addWidget(QLabel("Select Date:"))
        layout.addWidget(self.date_picker)

        buttons = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_task)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        buttons.addWidget(self.save_button)
        buttons.addWidget(self.cancel_button)

        layout.addLayout(buttons)
        self.setLayout(layout)

    def save_task(self):
        title = self.title_input.text()
        description = self.description_input.toPlainText()
        tag = self.tag_input.text()
        repeat = self.repeat_checkbox.isChecked()
        selected_date = self.date_picker.date().toString("yyyy-MM-dd")

        if title:
            self.task_manager.add_task(
                title=title,
                due_date=selected_date,
                tag=tag,
                description=description,
                repeat=repeat
            )
            self.accept()

    def get_selected_date(self):
        return self.date_picker.date().toString("yyyy-MM-dd")