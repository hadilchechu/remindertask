import os
import os.path
import sys
import sqlite3
import subprocess
from datetime import datetime, date, time

DB_NAME = 'rem.db'
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

header = """

				REMINDER                                                                  
"""

menu = """ 
	1. Create
	2. Update
	3. Delete
	4. View
	5. Exit
 							 
		"""

		
def create_table():
	cursor.executescript("""
		CREATE TABLE IF NOT EXISTS remind (
    	id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    	title    TEXT,
		create_date TEXT,
		remind_date TEXT);
		""")


def insert_rem(rem_name, rem_date):
	cursor.execute('''INSERT OR IGNORE INTO remind (
		title, create_date, remind_date) 
        VALUES ( ?, ?, ? )''', ( rem_name, str(datetime.now()).split('.')[0], rem_date)) 
	conn.commit()
	main_menu()

def create_rem():
	os.system('clear')
	current_year = datetime.now().year	
	remind_content = input('What you want to remind? ')
	rem_year = input('when.... Year  ')
	if int(rem_year) < current_year:
		input("This is not valid because the year less current year...! [Press ENTER]")
		update_rem()
	rem_month = input('Month (1-12)? ')
	rem_day = input('Day (1-31)? ')
	rem_hour = input('Hour (1-23)? ')
	rem_mind = input('Minute (0-59)? ')
	full_date = date(int(rem_year), int(rem_month), int(rem_day))
	full_time = time(int(rem_hour), int(rem_mind))
	combined_date = datetime.combine(full_date, full_time)
	print("reminder added for:",combined_date)
	print("Created at",str(datetime.now()))
	insert_rem(remind_content, combined_date)
	main_menu()

def view_rem(rec=0):
	if rec == 0:
		os.system('clear')
		cursor.execute("SELECT *FROM remind")
		data = cursor.fetchall()
		print("{0:5} {1:20} {2:25} {3:5} ".format("|id|", "|title|", "|created date     |",
				"|remind date      |"))
		for item in data:
			print("{0:5} {1:20} {2:25} {3:5} ".format(str(item[0]), item[1], item[2], item[3]))
		
	else:
		os.system('clear')
		cursor.execute("DELETE FROM remind WHERE id = ?", (rec, ))
		conn.commit()

		cursor.execute("SELECT *FROM remind")
		data = cursor.fetchall()
		
		print("{0:5} {1:20} {2:25} {3:5}".format("|id|", "|title|", "|created date|", "|remind date|"))
		for item in data:
			print("{0:5} {1:20} {2:25} {3:5} ".format(item[0], item[1], item[2], item[3]))
		main_menu()

def update_rem():

	current_year = datetime.now().year
	task_id = input(" ID? ")
	if int(task_id) == -99:
		main_menu()
	view_rem()
	print("\nUpdation\n")
	rem_content = input('What you want to remind? ')
	rem_year = input('Year..?  ')
	if int(rem_year) < current_year:
		input("This is not valid because the year less current year...! [Press ENTER]")
		update_rem()
	rem_month = input('Month (1-12)? ')
	rem_day = input('Day (1-31)? ')
	rem_hour = input('Hour (1-23)? ')
	rem_mind = input('Minute (0-59)? ')
	full_date = date(int(rem_year), int(rem_month), int(rem_day))
	full_time = time(int(rem_hour), int(rem_mind))
	combined_date = datetime.combine(full_date, full_time)

	cursor.execute('''UPDATE remind 
					SET title = ?,
					create_date = ?,
					remind_date = ? 
					WHERE id =?''',
					(rem_content, 
						str(datetime.now()).split('.')[0],
						combined_date,
						task_id)) 
	conn.commit()
	main_menu()

menuItems = [
    { "Create reminder": 1 },
    { "Update reminder": 2 },
	{ "Delete specific": 3 },
    { "View all": 4 },
	{ "Exit": 5 },
]
			
def main_menu():                                
	while True:
		print(header,"\n")
		print(menu,"\n")

		choice = input(">>> ")
		try:
			if int(choice) < 1: pass
			elif int(choice) == 1:
				create_rem()
			elif int(choice) == 2:
				update_rem()
			elif int(choice) == 3:
				view_rem(0)
				view_rem(input("For Delete... ENTER ID  "))
			elif int(choice) == 4:
				view_rem(0)
				main_menu()	
			elif int(choice) == 5:
				sys.exit(0)
			else:
				pass
		except ValueError:
			print("Invalid option")
			os.system('clear')
		except IndexError:
			print("Out of index")
			os.system('clear')

if __name__ == '__main__':
	
	create_table()
	main_menu()