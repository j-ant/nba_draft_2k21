import queries as qry
def show_menu():
  print("\nMAIN MENU")
  print("NBA DRAFT 2021-2022")
  print("==================")
  print("Choose an option from 1-6 or 0 to exit")
  print("1) Franchise with most rookie playing time")
  print("2) Which city does the given rookie come from?")
  print("3) Which rookies did the given team drafted?")
  print("4) How many rookies did not go to college?")
  print("5) List all the teams")
  print("6) List all the rookies")

  print("\n0) EXIT")

def get_user_input(n, cursor):
  try:
    n = int(n)
  except ValueError:
    print("Please enter an integer")
    return
  if n == 1:
    qry.team_rookie_max_minutes(cursor)
  elif n == 2:
    qry.get_rookie_city(cursor)
  elif n == 3:
    qry.get_rookies_by_team(cursor)
  elif n == 4:
    qry.rookies_no_college(cursor)
  elif n == 5:
    qry.list_all_teams(cursor)
  elif n == 6:
    qry.list_all_rookies(cursor)
  else:
      print("Wrong option")