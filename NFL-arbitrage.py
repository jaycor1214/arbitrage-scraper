from bs4 import BeautifulSoup
from selenium import webdriver
import re
from urllib.request import urlopen
from operator import attrgetter

# Get HTML

print("Scraping Fan Duel Data")
url = 'https://sportsbook.fanduel.com/navigation/nfl'
browser = webdriver.Chrome()
browser.get(url)
html_text = browser.page_source

soup = BeautifulSoup(html_text, 'lxml')

# Get teams
NFLarr = ['Arizona Cardinals',
'Atlanta Falcons',
'Baltimore Ravens',
'Buffalo Bills',
'Carolina Panthers',
'Chicago Bears',
'Cincinnati Bengals',
'Cleveland Browns',
'Dallas Cowboys',
'Denver Broncos',
'Detroit Lions',
'Green Bay Packers',
'Houston Texans',
'Indianapolis Colts',
'Jacksonville Jaguars',
'Kansas City Chiefs',
'Las Vegas Raiders',
'Los Angeles Chargers',
'Los Angeles Rams',
'Miami Dolphins',
'Minnesota Vikings',
'New England Patriots',
'New Orleans Saints',
'New York Giants',
'New York Jets',
'Philadelphia Eagles',
'Pittsburgh Steelers',
'San Francisco 49ers',
'Seattle Seahawks',
'Tampa Bay Buccaneers',
'Tennessee Titans',
'Washington Commanders',
'LV Raiders',
'JAX Jaguars',
'Jacksonville Jaguars',
'NY Jets',
'CIN Bengals',
'NE Patriots',
'BUF Bills',
'CHI Bears',
'SEA Seahawks',
'KC Chiefs',
'NY Giants',
'MIN Vikings',
'DET Lions',
'CAR Panthers',
'HOU Texans',
'TEN Titans',
'NO Saints',
'CLE Browns',
'ATL Falcons',
'BAL Ravens',
'WAS Commanders',
'SF 49ers',
'PHI Eagles',
'DAL Cowboys',
'LV Raiders',
'PIT Steelers',
'GB Packers',
'MIA Dolphins',
'DEN Broncos',
'LA Rams',
'TB Buccaneers',
'ARI Cardinals',
'LA Chargers',
'IND Colts']
teamArr = []
the_word = 'football'
tags = soup.find_all('a', href=lambda t: t and the_word in t, attrs={"target":"_self", "style":"cursor: pointer;"})
for tag in tags:
    names = tag.find_all('span')
    for name in names:
       if name.text in NFLarr:
            teamArr.append(name.text)

# Get lines
addNext = False
bets = soup.find_all('div', attrs={"role":"button", "style":"cursor: pointer;", "tabindex": "0"})
count = -1
count2 = -1
lineArr = []
for bet in bets:
    lines = bet.find_all('span')
    for line in lines:
        if line.text == 'Stats':
            count += 1
        if line.text == "NFL Draft":
            count = 5
        if count == 0 or count == 3:
            lineArr.append(line.text)
            if count == 0:
                count = 6
        if line.text[0] == 'O' or line.text[0] == 'U':
            count += 2
        count -= 1

browser.close()

print(len(lineArr))
print(len(teamArr))
# List should contain team, opponent, sportsbook, line

class event:
    def __init__(self, team, opponent, sportsbook, line, oppLine):
            self.team = team
            self.opponent = opponent
            self.sportsbook = sportsbook
            self.line = int(line)
            self.oppLine = int(oppLine)
    def func(self):
        print("Team: " + self.team + " Opponent: " + self.opponent + " Sportsbook: " + self.sportsbook + " Line: " + self.line)
FDevents = []
# build fan duel events
count = 0
if len(lineArr) == len(teamArr):
    while count < len(lineArr)-1:
        team1 = teamArr[count]
        team2 = teamArr[count+1]
        event1 = event(team1, team2, "FD", lineArr[count], lineArr[count+1])
        event2 = event(team2, team1, "FD", lineArr[count+1], lineArr[count])
        FDevents.append(event1)
        FDevents.append(event2)
        count += 2


# Now do Draft Kings

print("Scraping Draft Kings Data")
url = 'https://sportsbook.draftkings.com/leagues/football/nfl'
browser = webdriver.Chrome()
browser.get(url)
html_text = browser.page_source

teamArr = []
soup = BeautifulSoup(html_text, 'lxml')
teams = soup.find_all(attrs={"class":"event-cell__name-text"})

for team in teams:
    teamArr.append(team.text)

lineArr = []
count = 0
tags = soup.find_all('span',attrs={"class":"sportsbook-odds american default-color"})
for tag in tags:
    if(count % 2 == 0):
        tag = tag.text
        try:
            print(tag)
            lineArr.append(tag)
        except:
            tag = "-" + tag[1:len(tag)]
            lineArr.append(tag)
    count += 1

browser.close()
# team dictionary
apprevTeams = {
    "JAX Jaguars" : "Jacksonville Jaguars",
    "NY Jets" : "New York Jets",
    "CIN Bengals" : "Cincinnati Bengals",
    "NE Patriots" : "New England Patriots",
    "BUF Bills" : "Buffalo Bills",
    "CHI Bears" : "Chicago Bears",
    "SEA Seahawks" : "Seattle Seahawks",
    "KC Chiefs" : "Kansas City Chiefs",
    "NY Giants" : "New York Giants",
    "MIN Vikings" : "Minnesota Vikings",
    "DET Lions" : "Detroit Lions",
    "CAR Panthers" : "Carolina Panthers",
    "HOU Texans" : "Houstan Texans",
    "TEN Titans" : "Tennessee Titans",
    "NO Saints" : "New Orleans Saints", 
    "CLE Browns" : "Cleveland Browns",
    "ATL Falcons" : "Atlanta Falcons",
    "BAL Ravens" : "Baltimore Ravens",
    "WAS Commanders" : "Washington Commanders",
    "SF 49ers" : "San Francisco 49ers",
    "PHI Eagles" : "Philadelphia Eagles",
    "DAL Cowboys" : "Dallas Cowboys",
    "LV Raiders" : "Las Vegas Raiders",
    "PIT Steelers" : "Pittsburgh Steelers",
    "GB Packers" : "Greenbay Packers",
    "MIA Dolphins" : "Miami Dolphins",
    "DEN Broncos" : "Denver Broncos",
    "LA Rams" : "Las Angeles Chargers",
    "TB Buccaneers" : "Tampa Bay Buccaneers",
    "ARI Cardinals" : "Arizona Cardinals",
    "LA Chargers" : "Las Angeles Chargers",
    "IND Colts" : "Indianapolis Colts",
}

DKevents = []
count = 0
if len(lineArr) == len(teamArr):
    while count < len(lineArr)-1:
        try:
            team1 = apprevTeams[teamArr[count]]
        except: 
            team1 = teamArr[count]
        try:
            team2 = apprevTeams[teamArr[count+1]]
        except:
            team2 = teamArr[count+1]
        event1 = event(team1, team2, "DK", lineArr[count], lineArr[count+1])
        event2 = event(team2, team1, "DK", lineArr[count+1], lineArr[count])
        DKevents.append(event1)
        DKevents.append(event2)
        count += 2

# Bet Online
print("Scraping Bet Online Data")
url = 'https://www.betonline.ag/sportsbook/football/nfl'
browser = webdriver.Chrome()
browser.get(url)
html_text = browser.page_source

teamArr = []
soup = BeautifulSoup(html_text, 'lxml')

teams = soup.find_all('a',attrs={"class":"lines-row__link"})
for team in teams:
    for x in team:
        if x.text[1:len(x.text)] in NFLarr:
            teamArr.append(x.text[1:len(x.text)])

lineArr = []
count = 0
lines = soup.find_all('div', attrs={"class":"bet-pick__wager-line"})
for line in lines:
    if count == 0 or count == 3:
        lineArr.append(line.text)
    if count == 3:
        count = 0
    count += 1

#output arbitrage

class output:
    def __init__(self, team, opponent, arb1, arb2, sb1, sb2):
            self.team = team
            self.opponent = opponent
            self.arb1 = str(arb1)
            self.arb2 = str(arb2)
            self.sb1 = sb1
            self.sb2 = sb2
            self.sum = arb1 + arb2
    def show(self):
        print(self.team + " @ " + self.arb1 + " ON " + self.sb1)
        print(self.opponent + " @ " + self.arb2 + " ON " + self.sb2)
        print("results in: " + str(int(self.arb1) + int(self.arb2)))

arb = []
def compare(events1, events2, arb):
    for event1 in events1:
        team = event1.team
        opponent = event1.opponent
        for event2 in events2:
            if event2.team == team and event2.opponent == opponent:
                if event1.line > event2.line:
                    teamMax = event1.line
                    teamName = event1.team
                    sb1 = event1.sportsbook
                else:
                    teamMax = event2.line
                    teamName = event2.team
                    sb1 = event2.sportsbook
                if event1.oppLine > event2.oppLine:
                    oppMax = event1.oppLine
                    oppName = event1.opponent
                    sb2 = event1.sportsbook
                else:
                    oppMax = event2.oppLine
                    oppName = event2.opponent
                    sb2 = event2.sportsbook 

                theEvent = output(teamName, oppName, teamMax, oppMax, sb1, sb2)
                arb.append(theEvent)

compare(FDevents, DKevents, arb)

sorted_arb = sorted(arb, key = attrgetter('sum'))
sorted_arb.reverse()

for x in sorted_arb:
    x.show()



    






