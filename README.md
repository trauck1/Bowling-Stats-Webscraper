# Bowling-Stats-Webscraper

Bowling Score Scraper

When bowling at Crofton Bowling Centre, bowlers can enter their email and get their scores sent via a link.This Python script scrapes the bowling score data from the web-based score sheet and calculates the statistics for individual players.

**Features**

Web Scraping: Extracts bowling game data from HTML score sheets

Score Calculation: Accurately calculates bowling scores following official rules

Statistics Analysis: Provides detailed stats including:

Individual game scores
Average score across all games
Strike percentage and count
Spare percentage and count


Name Matching: Case-insensitive player name search
Data Validation: Filters out incomplete games

**Requirements**

Python 3.x
BeautifulSoup4
requests

**Usage**

Run the script:

python bowlingScoreWebScraper.py

When prompted, enter:

The URL of the bowling score sheet
The player name you want to analyze

**Test Links**

1)

https://www.syncpassport.com//MyScores/ScSession?eid=TBC&sessionIdentifier=bd521892116b4ee78b09dd49b427f87a

names- tim, big vince,kenn, j schmoney

2)

https://www.syncpassport.com//MyScores/ScSession?eid=TBC&sessionIdentifier=57512d0528274bd2af5bff89ebd9be53

names- guillermo, tim, Don

3)

https://www.syncpassport.com//MyScores/ScSession?eid=TBC&sessionIdentifier=4925dac1c53b4ad9a27f561b3cc5c42d

names- tim, mike

4)

https://www.syncpassport.com//MyScores/ScSession?eid=TBC&sessionIdentifier=a6961e3095504c53885fa9572427b698

names- tim, mike

**The script will output:**

Individual game scores
Average score
Strike statistics (count and opportunities)
Spare statistics (count and opportunities)



**Example Output**

John Doe:

Game 1 : 156

Game 2 : 189

Game 3 : 142

Average: 162.33

15 strikes out of 28 opportunities

8 spares out of 18 opportunities

**Game Formatting (gameFormatter)**

Converts raw HTML game data into structured format
Handles all 10 frames including special 10th frame rules
Processes different shot notations:

X = Strike (10 pins)
/ = Spare (remaining pins after first shot)
- = Miss (0 pins)
Numbers = Actual pin count


Filters out incomplete games

Score Calculation (calculateScores)

Implements official bowling scoring rules
Handles strikes, spares, and open frames
Accounts for bonus scoring:

Strike: 10 + next two shots
Spare: 10 + next shot
Open: Sum of two shots


Special 10th frame scoring logic

Statistics (calculateStats)

Counts total strikes and strike opportunities
Counts total spares and spare opportunities
Handles 10th frame complexities where multiple strikes/spares are possible
