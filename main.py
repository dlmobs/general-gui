import sys
from PySide2.QtCore import Qt, QFile, QTextStream
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QMessageBox, QFileDialog

class Checklist(QWidget):
    def __init__(self):
        super().__init__()

        self.items = []

        # Create GUI elements
        self.item_label = QLabel("Enter item:")
        self.item_input = QLineEdit()
        self.add_button = QPushButton("Add Item")
        self.checkboxes_layout = QVBoxLayout()
        self.checkboxes_widget = QWidget()
        self.reset_button = QPushButton("Reset Checklist")

        # Connect signals to slots
        self.add_button.clicked.connect(self.add_item)
        self.reset_button.clicked.connect(self.reset_checklist)
        self.item_input.returnPressed.connect(self.add_item)

        # Create layout
        main_layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.item_label)
        input_layout.addWidget(self.item_input)
        input_layout.addWidget(self.add_button)
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.checkboxes_widget)
        main_layout.addWidget(self.reset_button)
        self.setLayout(main_layout)

        # Load checklist if it exists
        self.load_checklist()

    def add_item(self):
        item = self.item_input.text()
        if item:
            self.items.append((item, False))
            self.item_input.clear()
            self.update_checkboxes()

    def update_checkboxes(self):
        for i in reversed(range(self.checkboxes_layout.count())):
            self.checkboxes_layout.itemAt(i).widget().setParent(None)
        for item, checked in self.items:
            checkbox = QCheckBox(item)
            checkbox.setChecked(checked)
            checkbox.stateChanged.connect(self.checkbox_state_changed)
            self.checkboxes_layout.addWidget(checkbox)
        self.checkboxes_widget.setLayout(self.checkboxes_layout)

    def checkbox_state_changed(self, state):
        checkbox = self.sender()
        index = self.checkboxes_layout.indexOf(checkbox)
        item, checked = self.items[index]
        self.items[index] = (item, checkbox.isChecked())

    def reset_checklist(self):
        self.items = []
        self.update_checkboxes()

    def closeEvent(self, event):
        if self.items:
            save = QMessageBox.question(self, "Save Checklist", "Do you want to save the checklist before closing?", QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Save)
            if save == QMessageBox.Save:
                file_path, _ = QFileDialog.getSaveFileName(self, "Save Checklist", "", "Text Files (*.txt);;All Files (*)")
                if file_path:
                    with open(file_path, 'w') as f:
                        for item, checked in self.items:
                            f.write(item + ',' + str(checked) + '\n')
            elif save == QMessageBox.Cancel:
                event.ignore()

    def load_checklist(self):
        file_path = "checklist.txt"
        if QFile.exists(file_path):
            with open(file_path, 'r') as f:
                for line in f:
                    item, checked = line.strip().split(',')
                    self.items.append((item, checked == 'True'))
                self.update_checkboxes()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    checklist = Checklist()
    checklist.show()
    sys.exit(app.exec_())
