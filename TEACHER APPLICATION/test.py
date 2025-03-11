import sys
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt

url = "http://127.0.0.1:8000"


class RollNumberWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Enter Roll Number")
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()

        # Roll number input field
        self.roll_number_input = QLineEdit()
        self.roll_number_input.setPlaceholderText("Enter Roll Number")
        layout.addWidget(self.roll_number_input)

        # Submit button to fetch student data
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.fetch_data)
        layout.addWidget(self.submit_button)

        # Label to show the result or error
        self.result_label = QLabel("")
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def fetch_data(self):
        """Fetch data from FastAPI server and display it in a new window."""
        roll_number = self.roll_number_input.text()

        if not roll_number.isdigit():
            self.result_label.setText("Please enter a valid roll number.")
            return

        try:
            # Request data from the FastAPI server
            response = requests.post(url+"/eiscore",json={"roll_no":roll_number})
            response.raise_for_status()  # Raise an exception for 4xx or 5xx errors

            student_data = response.json()
            self.display_student_data(student_data)

        except requests.exceptions.RequestException as e:
            self.result_label.setText(f"Error: {str(e)}")

    def display_student_data(self, student_data):
        """Display the student data in a new window."""
        self.student_window = StudentDataWindow(student_data)
        self.student_window.show()
        
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem

class StudentDataWindow(QWidget):
    def __init__(self, student_data):
        super().__init__()

        self.setWindowTitle("Student Data")
        self.setFixedSize(600, 400)
        print(student_data)
        layout = QVBoxLayout()

        # Create QTableWidget to display the student data
        self.table = QTableWidget(self)
        
        # Set the number of rows and columns based on the student_data
        self.table.setRowCount(len(student_data))  # Number of rows
        self.table.setColumnCount(len(student_data[0]))  # Number of columns (based on the first sublist)

        # Set the table headers
        self.table.setHorizontalHeaderLabels(["Time", "EI Score"])

        # Loop through the data and insert it into the table
        for row_index, row_data in enumerate(student_data):
            for col_index, cell_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(cell_data)))  # Ensure the data is a string
        
        # Add the table to the layout (only once, not inside the loop)
        layout.addWidget(self.table)

        # Set the layout for the window
        self.setLayout(layout)  # Set the layout once after all widgets have been added

def main():
    app = QApplication(sys.argv)
    window = RollNumberWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
