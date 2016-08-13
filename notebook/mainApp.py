
import sys
import re
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from models import *
from datetime import date
 
horHeaders = ['Fullname', 'Phone', 'Birthday', '', '']
 
class MyTable(QTableWidget):
    def __init__(self, *args):
        QTableWidget.__init__(self, *args)
        self.id_by_row = {}
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setHorizontalHeaderLabels(horHeaders)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
 
    def setData(self):

        row = 0
        for record in Record.select():
            self.id_by_row[row] = record.id 
            self.insertRow(self.rowCount())
            self.setItem(self.rowCount()-1, 0, QTableWidgetItem(str(record.name)))
            self.setItem(self.rowCount()-1, 1, QTableWidgetItem(str(record.phone)))
            self.setItem(self.rowCount()-1, 2, QTableWidgetItem(str(record.birthday)))

            self.button_edit = QPushButton('edit')
            self.button_edit.clicked.connect(self.handleEditButtonClicked)
            self.setCellWidget(self.rowCount()-1, 3, self.button_edit)
            
            self.button_delete = QPushButton('delete')
            self.button_delete.clicked.connect(self.handleDeleteButtonClicked)
            self.setCellWidget(self.rowCount()-1, 4, self.button_delete)

            row = row + 1    
    
    def handleDeleteButtonClicked(self):
        button = qApp.focusWidget()
        index = self.indexAt(button.pos())
        if index.isValid():
            instance = Record.get(Record.id == self.id_by_row[index.row()])
            instance.delete_instance()
            self.updateTable()

    def updateTable(self):
        self.setRowCount(0)
        self.id_by_row = {}
        self.setData()

    def handleEditButtonClicked(self):
        button = qApp.focusWidget()
        index = self.indexAt(button.pos())
        if index.isValid():
			edit = myEdit(table=self, id_contact=self.id_by_row[index.row()])
			edit.exec_()


class myEdit(QDialog):
    def __init__(self, table, id_contact, parent=None):
		QDialog.__init__(self, parent)
		self.table = table

		self.instance = Record.get(Record.id == id_contact)

		self.textName = QLineEdit(self.instance.name, self)
		self.textPhone = QLineEdit(str(self.instance.phone), self)
		self.textDate = QDateEdit(self)

		self.textDate.setDate(self.instance.birthday)
		self.textDate.setMaximumDate(QDate.currentDate())
		self.textDate.setCalendarPopup(True)

		self.buttonEdit = QPushButton('Apply', self)
		self.buttonEdit.clicked.connect(self.handleEdit)

		layout = QVBoxLayout(self)
		layout.addWidget(QLabel('Fullname'))
		layout.addWidget(self.textName)
		layout.addWidget(QLabel('Phone'))
		layout.addWidget(self.textPhone)
		layout.addWidget(QLabel('Birthday'))
		layout.addWidget(self.textDate)
		layout.addWidget(self.buttonEdit)

    def handleEdit(self):
		if (len(self.textName.text()) != 0 and len(self.textPhone.text()) != 0):
			pattern = r'^\d{6,15}$'
			phone_number = str(self.textPhone.text())
			if re.match(pattern, phone_number):
				year 	= self.textDate.date().year()
				month 	= self.textDate.date().month()
				day 	= self.textDate.date().day() 

				self.instance.name 	= str(self.textName.text())
				self.instance.phone = int(phone_number)
				self.instance.birthday = date(year, month, day)
				self.instance.save()
				
				self.table.updateTable()
				self.accept()
			else: QMessageBox.warning(self, 'Error', 'Invalid phone number')
		else: QMessageBox.warning(self, 'Error', 'Bad value') 

class MyForm(QWidget):
	def __init__(self, table, parent=None):
		QWidget.__init__(self, parent)
		self.setWindowTitle('NoteBook')
		self.table = table

		self.grid = QGridLayout()

		self.grid.addWidget(QLabel('Fullname'), 0, 0)
		self.grid.addWidget(QLabel('Phone'), 0, 1)
		self.grid.addWidget(QLabel('Birthday'), 0, 2)

		self.name = QLineEdit()
		self.name.setPlaceholderText('Fullname')
		self.phone = QLineEdit()
		self.phone.setPlaceholderText('789456123')


		self.dateEdit = QDateEdit(self)
		self.dateEdit.setDate(QDate.currentDate())
		self.dateEdit.setMaximumDate(QDate.currentDate())
		self.dateEdit.setCalendarPopup(True)

		self.commit = QPushButton('Add contact')
		self.commit.clicked.connect(self.handleAddButtonClicked)

		self.grid.addWidget(self.name, 1, 0)
		self.grid.addWidget(self.phone, 1, 1)
		self.grid.addWidget(self.dateEdit, 1, 2)
		self.grid.addWidget(self.commit, 1, 3)

	def initForm(self, name, phone, date):
		self.name.setText(name)
		self.phone.setText(phone)
		self.dateEdit.setDate(date)

	def getForm(self):
		return self.grid

	def handleAddButtonClicked(self):
	    if (len(self.name.text()) != 0 and len(self.phone.text()) != 0):
	    	pattern = r'^\d{6,15}$'
	    	phone_number = str(self.phone.text())
	    	if re.match(pattern, phone_number):
				name 	= str(self.name.text())
				ph 		= int(phone_number) 
				year 	= self.dateEdit.date().year()
				month 	= self.dateEdit.date().month()
				day 	= self.dateEdit.date().day()
				Record.create(name=name, phone=ph, birthday=date(year, month, day))
				self.myClear()
				self.table.updateTable()
	    	else: QMessageBox.warning(self, 'Error', 'Invalid phone number')
	    else: QMessageBox.warning(self, 'Error', 'Bad value')    

	def myClear(self):
		self.dateEdit.setDateTime(QDateTime.currentDateTime())
		self.name.clear()
		self.phone.clear()    

class MainApp(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowTitle('NoteBook')

        happy_string = "Don't forget to congratulate:\n"
        today = QDateTime.currentDateTime().date()
        for entry in Record.select().where(Record.birthday.day == today.day(),
        								Record.birthday.month == today.month()):
        	happy_string += "    " + entry.name + ": " + str(entry.phone) + "\n"

        if len(happy_string) > 0:
        	QMessageBox.information(self, 'Birthday reminder', happy_string)

        self.table = MyTable(0, 5)
        self.form = MyForm(table=self.table)

        grid = QGridLayout(self)
        grid.addLayout(self.form.getForm(), 0, 0)
        grid.addWidget(self.table, 1, 0)
        self.setLayout(grid)

    def myClear(self):
    	self.dateEdit.setDateTime(QDateTime.currentDateTime())
    	self.name.clear()
    	self.phone.clear()
 
def main(args):
    app = QApplication(args)

    start = MainApp()
    start.resize(600, 400)
    start.show()
    
    sys.exit(app.exec_())
 
if __name__=="__main__":
    main(sys.argv)