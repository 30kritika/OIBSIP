import sys
import random
import string
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QCheckBox, QSpinBox, QMessageBox
from PyQt5.QtGui import QClipboard

class PasswordGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Advanced Password Generator')

        layout = QVBoxLayout()

        self.length_label = QLabel('Password Length:', self)
        layout.addWidget(self.length_label)

        self.length_spinbox = QSpinBox(self)
        self.length_spinbox.setMinimum(8)
        self.length_spinbox.setMaximum(64)
        layout.addWidget(self.length_spinbox)

        self.include_uppercase = QCheckBox('Include Uppercase Letters', self)
        layout.addWidget(self.include_uppercase)

        self.include_numbers = QCheckBox('Include Numbers', self)
        layout.addWidget(self.include_numbers)

        self.include_special = QCheckBox('Include Special Characters', self)
        layout.addWidget(self.include_special)

        self.generate_button = QPushButton('Generate Password', self)
        self.generate_button.clicked.connect(self.generate_password)
        layout.addWidget(self.generate_button)

        self.password_display = QLineEdit(self)
        self.password_display.setReadOnly(True)
        layout.addWidget(self.password_display)

        self.copy_button = QPushButton('Copy to Clipboard', self)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        layout.addWidget(self.copy_button)

        self.setLayout(layout)
        self.show()
    
    def generate_password(self):
        length = self.length_spinbox.value()
        include_uppercase = self.include_uppercase.isChecked()
        include_numbers = self.include_numbers.isChecked()
        include_special = self.include_special.isChecked()

        if not (include_uppercase or include_numbers or include_special):
            QMessageBox.warning(self, 'Input Error', 'You must select at least one option for password complexity.')
            return

        password = self.create_password(length, include_uppercase, include_numbers, include_special)
        self.password_display.setText(password)

    def create_password(self, length, include_uppercase, include_numbers, include_special):
        characters = string.ascii_lowercase
        if include_uppercase:
            characters += string.ascii_uppercase
        if include_numbers:
            characters += string.digits
        if include_special:
            characters += string.punctuation

        password = ''.join(random.choice(characters) for _ in range(length))

        # Ensure the password includes at least one character from each selected category
        if include_uppercase:
            password = self.ensure_character(password, string.ascii_uppercase)
        if include_numbers:
            password = self.ensure_character(password, string.digits)
        if include_special:
            password = self.ensure_character(password, string.punctuation)

        return password

    def ensure_character(self, password, characters):
        password = list(password)
        password[random.randint(0, len(password) - 1)] = random.choice(characters)
        random.shuffle(password)
        return ''.join(password)

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.password_display.text())
        QMessageBox.information(self, 'Copied', 'Password copied to clipboard!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PasswordGenerator()
    sys.exit(app.exec_())
