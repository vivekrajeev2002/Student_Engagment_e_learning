import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
    QStackedWidget, QMessageBox, QFormLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import requests
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QColor
tr_name=""
url = "http://127.0.0.1:8000"
w=1000
h=700

class WelcomeScreen(QWidget):
    """ Welcome Screen """
    def __init__(self):
        super().__init__()
        
        # Set window size and style
        self.setFixedSize(w, h)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;  /* Dark navy background */
                color: white;
                font-family: Arial, sans-serif;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(30)  # More spacing between elements

        # Title label with modern styling
        self.label = QLabel("🎓 Student Engagement Detection - Teacher Application 🎓", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
            font-size: 36px;
            font-weight: bold;
            color: #4CAF50;
            padding :20
        """)

        # Login button with a modern flat design
        self.login_button = QPushButton("🔑 Login")
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 22px;
                font-weight: bold;
                padding: 20px 40px;
                border-radius: 20px;
                border: 2px solid #45a049;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #387a3f;
            }
        """)
        self.login_button.clicked.connect(self.go_to_login)

        # Adding widgets to the layout
        layout.addStretch()
        layout.addWidget(self.label)
        layout.addSpacing(100)
        layout.addWidget(self.login_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        self.setLayout(layout)

    def go_to_login(self):
        self.st = LoginScreen()  # Assuming LoginScreen is defined
        self.close()
        self.st.show()

class LoginScreen(QWidget):
    """ Login Screen """
    def __init__(self):
        super().__init__()

        self.setFixedSize(w, h)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: white;
                font-family: Arial, sans-serif;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Title label
        self.label = QLabel("🔐 Login to Continue")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
        """)

        # Username input
        self.username = QLineEdit()
        self.username.setPlaceholderText("👤 Username")
        self.username.setStyleSheet("""
            QLineEdit {
                background-color: #2c2f36;
                color: white;
                font-size: 18px;
                padding: 12px;
                border: 2px solid #4CAF50;
                border-radius: 10px;
            }
        """)

        # Password input
        self.password = QLineEdit()
        self.password.setPlaceholderText("🔑 Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setStyleSheet("""
            QLineEdit {
                background-color: #2c2f36;
                color: white;
                font-size: 18px;
                padding: 12px;
                border: 2px solid #4CAF50;
                border-radius: 10px;
            }
        """)

        # Login button
        self.login_button = QPushButton("🚀 Login")
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 20px;
                font-weight: bold;
                padding: 15px;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #387a3f;
            }
        """)
        self.login_button.clicked.connect(self.authenticate)

        # Register button
        self.register_button = QPushButton("📝 Register")
        self.register_button.setStyleSheet("""
            QPushButton {
                background-color: #3a3f51;
                color: white;
                font-size: 20px;
                font-weight: bold;
                padding: 15px;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #50566d;
            }
            QPushButton:pressed {
                background-color: #2c2f36;
            }
        """)
        self.register_button.clicked.connect(self.trreg)

        layout.addStretch()
        layout.addWidget(self.label)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)
        layout.addStretch()

        self.setLayout(layout)

    def authenticate(self):
        username = self.username.text()
        password = self.password.text()
        response = requests.post(url + "/teacher", json={"usr": username, "pas": password})
        if response.status_code == 200:
            data = response.json()
            if data["ath"] == 2:
                self.st = TeacherScreen()
                self.st.show()
                self.close()
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid username or password!")
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password!")

    def trreg(self):
        self.st = TeacherRegistration()
        self.st.show()


class TeacherRegistration(QWidget):
    """Teacher Registration Screen"""
    def __init__(self):
        super().__init__()

        self.setWindowTitle("👩‍🏫 Teacher Registration")
        self.setFixedSize(600, 400)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: white;
                font-family: Arial, sans-serif;
            }
        """)

        layout = QFormLayout()
        layout.setSpacing(20)

        # Styled input fields
        self.name_input = self.create_input("👤 Full Name")
        self.emailid_input = self.create_input("📧 Email Address")
        self.password_input = self.create_input("🔑 Password", is_password=True)
        self.institute_name = self.create_input("🏫 Institute Name")

        # Register button
        self.submit_button = QPushButton("🚀 Register")
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 12px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #387a3f;
            }
        """)
        self.submit_button.clicked.connect(self.register_teacher)

        # Add fields to layout
        layout.addRow("👤 Name:", self.name_input)
        layout.addRow("📧 Email:", self.emailid_input)
        layout.addRow("🔑 Password:", self.password_input)
        layout.addRow("🏫 Institute:", self.institute_name)
        layout.addRow(self.submit_button)

        self.setLayout(layout)

    def create_input(self, placeholder, is_password=False):
        """Helper method to create styled input fields."""
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setStyleSheet("""
            QLineEdit {
                background-color: #2c2f36;
                color: white;
                font-size: 16px;
                padding: 10px;
                border: 2px solid #4CAF50;
                border-radius: 8px;
            }
        """)
        if is_password:
            input_field.setEchoMode(QLineEdit.EchoMode.Password)
        return input_field

    def register_teacher(self):
        """Handle teacher registration."""
        name = self.name_input.text()
        email_id = self.emailid_input.text()
        password = self.password_input.text()
        institute = self.institute_name.text()

        if name and email_id and password and institute:
            response = requests.post(url + "/teacher/reg", json={
                "name": name, "email": email_id, "password": password, "institute": institute
            })
            if response.status_code == 200:
                QMessageBox.information(self, "✅ Success", f"Teacher {name} registered successfully!")
            else:
                QMessageBox.warning(self, "⚠️ Error", f"Teacher {name} already registered!")
        else:
            QMessageBox.warning(self, "⚠️ Error", "All fields are required!")
class RollNumberWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("🎓 Enter Roll Number")
        self.setFixedSize(600, 300)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: white;
                font-family: Arial, sans-serif;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Title label
        title = QLabel("🔍 Fetch Student Data")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        # Roll number input
        self.roll_number_input = QLineEdit()
        self.roll_number_input.setPlaceholderText("📄 Enter Roll Number")
        self.roll_number_input.setStyleSheet("""
            QLineEdit {
                background-color: #2c2f36;
                color: white;
                font-size: 18px;
                padding: 12px;
                border: 2px solid #4CAF50;
                border-radius: 10px;
            }
        """)

        # Class ID input
        self.clsid = QLineEdit()
        self.clsid.setPlaceholderText("🏫 Enter Class ID")
        self.clsid.setStyleSheet("""
            QLineEdit {
                background-color: #2c2f36;
                color: white;
                font-size: 18px;
                padding: 12px;
                border: 2px solid #4CAF50;
                border-radius: 10px;
            }
        """)

        # Submit button
        self.submit_button = QPushButton("🚀 Submit")
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 20px;
                font-weight: bold;
                padding: 15px;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #387a3f;
            }
        """)
        self.submit_button.clicked.connect(self.fetch_data)

        # Result label
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("font-size: 18px;")

        # Add widgets to layout
        layout.addWidget(title)
        layout.addWidget(self.roll_number_input)
        layout.addWidget(self.clsid)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def fetch_data(self):
        """Fetch data from FastAPI server and display it in a new window."""
        roll_number = self.roll_number_input.text()
        cid = self.clsid.text()
        if roll_number and cid:
            response = requests.post(url + "/eiscore", json={"roll_no": roll_number, "clsid": cid})
            if(response.status_code==200 and response.json()):
                student_data = response.json()
                self.display_student_data(student_data)
            else:
                self.result_label.setText("❌ Error ")
        else:
            self.result_label.setText("Enter Valid roll no and Calssid")

    def display_student_data(self, student_data):
        """Display the student data in a new window."""
        self.student_window = StudentDataWindow(student_data)
        self.student_window.show()

class StudentDataWindow(QWidget):
    def __init__(self, student_data):
        super().__init__()

        self.setWindowTitle("📊 Student Data")
        self.setFixedSize(800, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: white;
                font-family: Arial, sans-serif;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Title label
        title = QLabel("📈 Engagement Insights")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 10px;
        """)

        # Create QTableWidget with modern styling
        self.table = QTableWidget(self)
        self.table.setRowCount(len(student_data))
        self.table.setColumnCount(len(student_data[0]))
        self.table.setHorizontalHeaderLabels(["⏰ Time", "📊 EI Score","Status"])
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 300)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #2c2f36;
                border: 2px solid #4CAF50;
                gridline-color: #4CAF50;
                font-size: 18px;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 5px;
                border: 1px solid #45a049;
            }
            QTableWidget::item {
                padding: 10px;
            }
        """)

        # Populate the table
        for row_index, row_data in enumerate(student_data):
            for col_index, cell_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(cell_data)))

        # Add widgets to layout
        layout.addWidget(title)
        layout.addWidget(self.table)
        self.setLayout(layout)
    
class TeacherScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Teacher Dashboard")
        self.setFixedSize(w,h)

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
        self.res = RollNumberWindow()
        self.res.show()

class StudentRegistrationScreen(QWidget):
    """Student Registration Screen"""
    def __init__(self):
        super().__init__()

        self.setWindowTitle("📝 Student Registration")
        self.setFixedSize(600, 400)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: white;
                font-family: Arial, sans-serif;
            }
        """)

        layout = QFormLayout()
        layout.setSpacing(20)

        # Input fields with modern style
        self.name_input = self.create_input("👤 Full Name")
        self.roll_no_input = self.create_input("📄 Roll Number")
        self.email = self.create_input("📧 Email Address")

        # Submit button with modern styling
        self.submit_button = QPushButton("🚀 Register")
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 12px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #387a3f;
            }
        """)
        self.submit_button.clicked.connect(self.register_student)

        # Add fields and button to layout
        layout.addRow("👤 Name:", self.name_input)
        layout.addRow("📄 Roll No:", self.roll_no_input)
        layout.addRow("📧 Email:", self.email)
        layout.addRow(self.submit_button)

        self.setLayout(layout)

    def create_input(self, placeholder):
        """Helper method to create styled input fields."""
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setStyleSheet("""
            QLineEdit {
                background-color: #2c2f36;
                color: white;
                font-size: 16px;
                padding: 10px;
                border: 2px solid #4CAF50;
                border-radius: 8px;
            }
        """)
        return input_field

    def register_student(self):
        """Handle student registration."""
        name = self.name_input.text()
        roll_no = self.roll_no_input.text()
        email = self.email.text()

        if name and roll_no and email:
            response = requests.post(url + '/student_reg', json={"name": name, "roll_no": roll_no, "email": email})
            if response.status_code == 200:
                QMessageBox.information(self, "✅ Success", f"Student {name} registered successfully!")
            else:
                QMessageBox.warning(self, "❌ Error", "Problem registering student")
        else:
            QMessageBox.warning(self, "⚠️ Error", "All fields are required!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = WelcomeScreen()
    main_window.setWindowTitle("Student Registration System")
    main_window.show()
    sys.exit(app.exec())
