import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
    QStackedWidget, QMessageBox, QFormLayout
)
from PyQt6.QtCore import Qt
import requests
tr_name=""
url = "http://127.0.0.1:8000"
w=1000
h=700
class WelcomeScreen(QWidget):
    """ Welcome Screen """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setFixedSize(w,h)
        self.label = QLabel("Welcome to the Student Registration System!", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        self.label.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.go_to_login)

        layout.addWidget(self.label)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

    def go_to_login(self):
        #self.stacked_widget.setCurrentIndex(1)  # Switch to login screen
        self.st= LoginScreen()
        self.close()
        self.st.show()

class LoginScreen(QWidget):
    """ Login Screen """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setFixedSize(w,h)
        self.label = QLabel("Login to Continue")
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.authenticate)

        self.register_button=QPushButton("Register")
        self.register_button.clicked.connect(self.trreg)

        layout.addWidget(self.label)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)
        self.setLayout(layout)

    def authenticate(self):
        username = self.username.text()
        password = self.password.text()
        username= username
        response = requests.post(url+"/teacher",json={"usr":username,"pas":password})
        if(response.status_code == 200):
            data=response.json()
            print(data)
            if(data["ath"]==2):
                self.st = StudentRegistrationScreen()
                self.st.show()
                self.close()
            else:
                print("Authentication failed")
                QMessageBox.warning(self, "Login Failed", "Invalid username or password!")        
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password!")
    def trreg(self):
        self.st=TeacherRegistration()
        self.st.show()

class TeacherRegistration(QWidget):
    def __init__(self):
        super().__init__()
        layout = QFormLayout()
        self.setFixedSize(w,h)
        self.name_input = QLineEdit()
        self.emailid_input = QLineEdit()
        self.password_input = QLineEdit()
        self.institute_name = QLineEdit()
        self.submit_button = QPushButton("Register")
        self.submit_button.clicked.connect(self.register_teacher)

        layout.addRow("Name", self.name_input)
        layout.addRow("Roll No", self.emailid_input)
        layout.addRow("Class", self.password_input)
        layout.addRow("Institue Name",self.institute_name)
        layout.addRow(self.submit_button)
        self.setLayout(layout)

    def register_teacher(self):
        name = self.name_input.text()
        email_id = self.emailid_input.text()
        password = self.password_input.text()
        ints = self.institute_name.text()
        if(self.name_input and self.emailid_input and self.password_input and self.institute_name):
            response=requests.post(url+"/teacher/reg",json ={"name":name,"email":email_id,"password":password,"ints":institute})
            print(response)
            QMessageBox.information(self, "Success", f"Student {name} registered successfully!")
        else:
            QMessageBox.warning(self, "Error", "All fields are required!")








class StudentRegistrationScreen(QWidget):
    """ Stuwdent Registration Screen """
    def __init__(self):
        super().__init__()
        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.roll_no_input = QLineEdit()
        self.class_input = QLineEdit()
        self.age_input = QLineEdit()

        self.submit_button = QPushButton("Register")
        self.submit_button.clicked.connect(self.register_student)

        layout.addRow("Name:", self.name_input)
        layout.addRow("Roll No:", self.roll_no_input)
        layout.addRow("Class:", self.class_input)
        layout.addRow("Age:", self.age_input)
        layout.addRow(self.submit_button)

        self.setLayout(layout)

    def register_student(self):
        name = self.name_input.text()
        roll_no = self.roll_no_input.text()
        class_name = self.class_input.text()
        age = self.age_input.text()

        if name and roll_no and class_name and age:
            QMessageBox.information(self, "Success", f"Student {name} registered successfully!")
        else:
            QMessageBox.warning(self, "Error", "All fields are required!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = WelcomeScreen()
    main_window.setWindowTitle("Student Registration System")
    main_window.show()
    sys.exit(app.exec())
