import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
    QStackedWidget, QMessageBox, QFormLayout
)
from PyQt6.QtGui import QFont
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
                self.st = TeacherScreen()
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

class TeacherScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Teacher Dashboard")
        self.setFixedSize(600, 400)

        # Layout setup
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Title Label
        title = QLabel("Teacher Dashboard")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Class link input
        self.link = QLineEdit()
        self.link.setPlaceholderText("Paste the online class link here")
        self.link.setFont(QFont("Arial", 12))
        self.link.setStyleSheet("padding: 8px; border-radius: 8px; border: 1px solid #ccc;")

        # Class ID input
        self.clsid = QLineEdit()
        self.clsid.setPlaceholderText("Enter Class ID")
        self.clsid.setFont(QFont("Arial", 12))
        self.clsid.setStyleSheet("padding: 8px; border-radius: 8px; border: 1px solid #ccc;")

        # Buttons
        self.upload = QPushButton("Upload Class Details")
        self.upload.setFont(QFont("Arial", 12))
        self.upload.setStyleSheet("background-color: #5cb85c; color: white; padding: 8px; border-radius: 8px;")
        self.upload.clicked.connect(self.uploadlink)

        self.student_reg = QPushButton("Student Registration")
        self.student_reg.setFont(QFont("Arial", 12))
        self.student_reg.setStyleSheet("background-color: #0275d8; color: white; padding: 8px; border-radius: 8px;")
        self.student_reg.clicked.connect(self.register)

        self.result = QPushButton("View Result")
        self.result.setFont(QFont("Arial", 12))
        self.result.setStyleSheet("background-color: #f0ad4e; color: white; padding: 8px; border-radius: 8px;")
        self.result.clicked.connect(self.viewresult)

        # Add widgets to layout
        layout.addWidget(title)
        layout.addWidget(self.link)
        layout.addWidget(self.clsid)
        layout.addWidget(self.upload)
        layout.addWidget(self.student_reg)
        layout.addWidget(self.result)

        # Set layout for the widget
        self.setLayout(layout)

    # Placeholder for the upload function
    def uploadlink(self):
        print("Uploading class details")
        print(self.clsid.text(),self.link.text())
        requests.post(url+"/classlink",json={"clsid":self.clsid.text(),"link":self.link.text()})
    # Placeholder for the register function
    def register(self):
        self.std = StudentRegistrationScreen()
        self.std.show()

    # Placeholder for the view result function
    def viewresult(self):
        print("Viewing result")

class StudentRegistrationScreen(QWidget):
    """ Stuwdent Registration Screen """
    def __init__(self):
        super().__init__()
        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.roll_no_input = QLineEdit()
        self.email = QLineEdit()

        self.submit_button = QPushButton("Register")
        self.submit_button.clicked.connect(self.register_student)

        layout.addRow("Name:", self.name_input)
        layout.addRow("Roll No:", self.roll_no_input)
        layout.addRow("email:", self.email)
        layout.addRow("Submit",self.submit_button)  

        self.setLayout(layout)

    def register_student(self):
        name = self.name_input.text()
        roll_no = self.roll_no_input.text()
        email = self.email.text()
        response = requests.post(url+'/student_reg',json={"name":name,"roll_no":roll_no,"email":email})
        if name and roll_no and email:
            if response.status_code==200:
                QMessageBox.information(self, "Success", f"Student {name} registered successfully!")
            else:
                QMessageBox.warning(self, "Error", "Problem in  registering student")        
        else:
            QMessageBox.warning(self, "Error", "All fields are required!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = WelcomeScreen()
    main_window.setWindowTitle("Student Registration System")
    main_window.show()
    sys.exit(app.exec())
