from turtle import st


# Which franchise has most rookie playing time?
# Get the team with the most sum of all of the rookies'
# playing time
def team_rookie_max_minutes(c):
  __create_rookie_team_view(c)
  __create_group_by_team(c)

  statement = ('''SELECT 
  franchise
  FROM 
  rookie_team_playtime
  ORDER BY total_rookie_minutes
  DESC LIMIT 0,1
  ''')

  c.execute(statement)
  rookie_minutes = c.fetchall()

  for minute in rookie_minutes:
    team = minute[0]
  print(team)

# view of rookies and their franchise/team
def __create_rookie_team_view(c):
  statement = ('''
  CREATE OR REPLACE VIEW rookie_team AS
  SELECT 
    rookies.*,
    teams.franchise_name AS franchise
  FROM rookies
  JOIN teams ON rookies.team=teams.name_abrv
  ''')
  c.execute(statement)

# Group rookie playtime by team
def __create_group_by_team(c):
  statement = ('''
  CREATE OR REPLACE VIEW rookie_team_playtime AS
  SELECT 
    franchise,
    sum(minutes_played) AS total_rookie_minutes
  FROM nba_draft.rookie_team
  GROUP BY franchise
  ''')
  c.execute(statement)

# Which city does the rookie with most points come from? 
# (Assuming rookies are from the same city as they went to college)
def get_rookie_city(c):
  __rookie_college_view(c)
  rookie_name = input('Enter rookie name: ')
  statement = f'''
  SELECT player_name,
  city
  FROM rookie_college_city
  WHERE player_name='{rookie_name}'
  '''
  c.execute(statement)
  city_tuple = c.fetchall()
  city = None

  for ct in city_tuple:
    player = ct[0]
    city = ct[1]

  error_msg = "Rookie unavailable or rookie did not attend college"
  print(error_msg) if city == None else print(f"{player} is from {city}")

def __rookie_college_view(c):
  statement = f'''
  CREATE OR REPLACE VIEW rookie_college_city AS 
  SELECT 
    rookies.player_name,
    colleges.name,
    colleges.city
  FROM rookies
  LEFT JOIN colleges ON rookies.college = colleges.name
  '''
  c.execute(statement)

# college that 
def get_rookies_by_team(c):
  __create_rookie_team_view(c)
  print("Get rookies and their stats by entering team name")
  team_name = input('Enter team name (either franchise name or team name abbrevation): ') 
  statement = f'''
  SELECT 
    player_name,
    games_played,
    minutes_played,
    points,
    rebounds,
    assists
  FROM rookie_team
  WHERE '{team_name}' = franchise OR '{team_name}' = team
  '''
  c.execute(statement)
  rookies = c.fetchall()
  for rookie in rookies:
    rook_stats = [rookie_stats for rookie_stats in rookie]
    print(f'''\nName: {rook_stats[0]}
  Games Played: {rook_stats[1]}
  Minutes Played: {rook_stats[2]}
  Points: {rook_stats[3]}
  Rebounds: {rook_stats[4]}
  Assists: {rook_stats[5]}''')

def rookies_no_college(c):
  statement = f'''
  SELECT COUNT(*)
  AS null_count
  FROM rookies
  WHERE college IS NULL
  '''
  c.execute(statement)
  null_count = c.fetchall()

  for null in null_count:
    rookie_wo_college = null[0]

  print(f'''Number of rookies that did not go to college: {rookie_wo_college}''')

def list_all_teams(c):
  statement = "SELECT name_abrv,franchise_name FROM teams"
  c.execute(statement)
  nba_teams = c.fetchall()

  print("\nNBA TEAMS\n===========")
  for team in nba_teams:
    print(f"{team[0]} - {team[1]}")

def list_all_rookies(c):
  __create_rookie_team_view(c)
  statement = "SELECT player_name, franchise FROM rookie_team"
  c.execute(statement)
  rookies = c.fetchall()

  print("\nROOKIES\n==========")
  for rookie in rookies:
    print(f"{rookie[0]}  -  {rookie[1]}")