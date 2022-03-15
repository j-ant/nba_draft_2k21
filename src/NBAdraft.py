# Jeremiah ante
# ja224uh@student.lnu.se

import mysql.connector
import csv
import os
import menu

cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1')
DB_NAME = "nba_draft"
cursor = cnx.cursor()

def table_not_exist(table_name):
  cursor.execute("SHOW TABLES")
  tables = cursor.fetchall()
  
  for table in tables:
    if string_strip(table) == table_name:
      return False
  return True

def string_strip(name):
  name = str(name)
  return name.strip("'( ,)")

def create_rookies_table():
  rookies_table = ('''
    CREATE TABLE Rookies (
      pick_number int NOT NULL,
      team varchar(45),
      player_name varchar(45),
      college varchar(45),
      games_played int,
      minutes_played int,
      points int,
      rebounds int,
      assists int,
      PRIMARY KEY (pick_number),
      FOREIGN KEY (college) REFERENCES colleges(name),
      FOREIGN KEY (team) REFERENCES teams(name_abrv)
    )
  ''')
  cursor.execute(rookies_table)

def create_teams_table():
  teams_table = ('''
    CREATE TABLE Teams (
      name_abrv varchar(45) NOT NULL,
      franchise_name varchar(45),
      date_founded varchar(45),
      games_played varchar(45),
      wins int,
      losses int,
      playoff_participation int,
      championships_won int,
      PRIMARY KEY (franchise_name)
    )
  ''')
  cursor.execute(teams_table)

def create_colleges_table():
  colleges_table = ('''
    CREATE TABLE Colleges (
      name varchar(45) NOT NULL,
      city varchar(45),
      year_founded int,
      PRIMARY KEY (name)
    )
  ''')
  cursor.execute(colleges_table)

def create_tables():
  if table_not_exist("teams"):
    create_teams_table()

  if table_not_exist("colleges"):
    create_colleges_table()
  
  if table_not_exist("rookies"):
    create_rookies_table()

def insert_data(data, table_name):
  next(data)
  for row in data:
    counter = 0
    for field in row:
      if field == '':
        row[counter] = None
      counter += 1
    if table_name == "teams":
      cursor.execute("INSERT IGNORE INTO Teams VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", row)

    if table_name == "colleges":
      cursor.execute("INSERT IGNORE INTO Colleges VALUES (%s, %s, %s)", row)

    if table_name == "rookies":
      cursor.execute("INSERT IGNORE INTO Rookies VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", row)
  cnx.commit()

def import_data():
  team_data = csv.reader(open('data/teams.csv'))
  rookies_data = csv.reader(open('data/rookies.csv'))
  colleges_data = csv.reader(open('data/colleges.csv'))

  insert_data(team_data, "teams")
  insert_data(colleges_data, "colleges")
  insert_data(rookies_data, "rookies")

def init_db():
  cursor.execute(f'CREATE DATABASE IF NOT EXISTS {DB_NAME}')
  cursor.execute(f'USE {DB_NAME}')
  create_tables()
  import_data()

init_db()

while True:
  menu.show_menu()
  n = input('Choose an option: ')
  if n == '0':
      break
  menu.get_user_input(n, cursor)
  print("\nPress any key to continue...")
  os.system('pause >nul')
cnx.close()
cursor.close()

print("Program exit...")