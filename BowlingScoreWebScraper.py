from bs4 import BeautifulSoup
import requests

def getCorrectGames(url, name):
    correctGames=[]
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    scoreTable = soup.find_all('table', {'class','ss-data'})
    for table in scoreTable:
        #rows of the the individual games in the game table
        gameRows = table.find_all('tr',{'class','notranslate'})
        for game in gameRows:
            #find the game that matches with the given name
            currentName = game.find('td',{'class','cls_player'}).text
            #capitalization doesn't matter
            if(name.lower() == currentName.lower()):
                correctGames.append(game)
    return correctGames


def gameFormatter(games):
    formattedGames = []
    for game in games:
        #first nine frames have the same name, but the tenth frame is named differently
        firstNine = game.find_all('td', {'class','cls_frame'})
        tenthFrame = game.find('td',{'class','cls_frame10'})
        invalidGame = False
        currentGame = []
        for i in range(10):
            #if it isn't the tenth frame, there isn't a thirdThrow to find
            if(i < 9):
                firstThrow = firstNine[i].find('td',{'class','cls_ball1'})
                secondThrow = firstNine[i].find('td',{'class','cls_ball2'})
            #tenth frame
            thirdThrow = 0
            if(i == 9):
                firstThrow = tenthFrame.find('td',{'class','cls_ball1'})
                secondThrow = tenthFrame.find('td',{'class','cls_ball2'})
                thirdThrow = tenthFrame.find('td',{'class', 'cls_ball3'})
            frame = []
            
            #all the possible outcomes for the first shot
            if(firstThrow):
                if(firstThrow.text == 'X'):
                    frame.append(10)
                elif(firstThrow.text == '-'):
                    frame.append(0)
                #this indicates this game is incomplete
                elif(firstThrow.text == ' ' or firstThrow.text == ''):
                    invalidGame = True
                else:
                    frame.append(int(firstThrow.text))
            else:
                invalidGame = True
            
            #all possible outcomes for the second shot
            if(secondThrow):
                
                #strike only possible for secondThrow in the tenth frame
                if(secondThrow.text == 'X'):
                    frame.append(10)
                elif(secondThrow.text == '-' or secondThrow.text == ' ' or secondThrow.text == ''):
                    frame.append(0)
                elif(secondThrow.text == '/'):
                    if(firstThrow.text == '-'):
                        frame.append(10)
                    else:
                        #finds the number of pins down using the first shot
                        score = 10 - int(firstThrow.text)
                        frame.append(score)
                else:
                    frame.append(int(secondThrow.text))
            
            #tenth frame
            if(i == 9):    
                
                #all possible outcomes for the third shot
                if(thirdThrow):
                    if(thirdThrow.text == 'X'):
                        frame.append(10)
                    elif(thirdThrow.text == '-' or thirdThrow.text == ' ' or thirdThrow.text == ''):
                        frame.append(0)
                    elif(thirdThrow.text == '/'):
                        if(secondThrow.text == '-'):
                            frame.append(10)
                        else:
                            score = 10 - int(secondThrow.text)
                            frame.append(score)
                    else:
                        frame.append(int(thirdThrow.text))
            currentGame.append(frame)
            #reset the frame list
            frame = []
        
        #if the game was finished to completion, add it to the list of games
        if(not invalidGame):
            formattedGames.append(currentGame)
        #reset the invalid game checker and the currentGame list
        invalidGame = False
        currentGame = []
    return formattedGames
            
def calculateScores(game):
    totalScore = 0
    prevShot = 0 #0-open,1-spare,2-strike
    twoStrikes = False
    
    #loops through 10 frames
    for i in range(10):
        firstShot = 0
        secondShot = 0
        thirdShot = 0
        
        #gets the amount of pins per shot
        if game[i][0]:
            firstShot = game[i][0]
        if len(game[i]) >= 2:
            secondShot = game[i][1]
        if i == 9 and len(game[i]) == 3:
            thirdShot = game[i][2]
        #last shot was open
        if prevShot == 0:
            totalScore += int(firstShot)
            totalScore += int(secondShot)
        #last shot was a spare
        elif prevShot == 1:
            totalScore += (int(firstShot) * 2)
            totalScore += int(secondShot)
        #last shot was a strike
        elif prevShot == 2:
            #last two shots were strikes
            if twoStrikes:
                totalScore += (int(firstShot) * 3)
                totalScore += (int(secondShot) * 2)
            else:
                totalScore += (int(firstShot) * 2)
                totalScore += (int(secondShot) * 2)
        if(int(firstShot) + int(secondShot)) >= 10:
            if int(firstShot) == 10:
                if prevShot == 2:
                    twoStrikes = True
                prevShot = 2
                
            else:
                prevShot = 1
                twoStrikes = False
        else: 
            prevShot = 0
            twoStrikes = False
        totalScore += int(thirdShot)
    return totalScore


def calculateStats(games):
    strikes = 0
    strikeOpportunity = 0
    spares = 0
    spareOpportunity = 0
    
    for game in games:
        for i in range(10):
            strikeOpportunity+=1
            firstShot = 0
            secondShot = 0
            thirdShot = 0
            
            #gets the amount of pins per shot if that shot exists
            if game[i][0]:
                firstShot = game[i][0]
            if len(game[i]) >= 2:
                secondShot = game[i][1]
            if i == 9 and len(game[i]) == 3:
                thirdShot = game[i][2]
            
            #got the strike
            if(int(firstShot) == 10):
                strikes+=1
                #tenth frame
                if(i==9):
                    #if the first shot was a strike in the 10th frame, another chance at a strike
                    strikeOpportunity+=1
                    if(int(secondShot) == 10):
                        strikes+=1
                        
                        #if the second shot was also a strike in the 10th, thats another strike opportunity
                        strikeOpportunity+=1
                        if(int(thirdShot == 10)):
                            strikes+=1
                    else:
                        spareOpportunity+=1
                        if(int(secondShot)+int(thirdShot) == 10):
                            spares+=1
            #didn't get the strike(chance for a spare)
            else:
                spareOpportunity+=1
                if(int(firstShot) + int(secondShot) == 10):
                    spares+=1
                    if(i==9):
                        strikeOpportunity+=1
                        if(int(thirdShot) == 10):
                            strikes+=1
    print(strikes, 'strikes out of ', strikeOpportunity, 'opportunities')
    print(spares, 'spares out of ', spareOpportunity, 'opportunities')
    
#gets the average from all the scores
def avg(scores):
    total = 0
    for score in scores:
        total +=score
    return (total / len(scores))

if __name__ == "__main__":
    #url from Crofton Bowling Score Sheet
    url = input("Enter the link you would like to use: ")
    name = input("What name would you like scores for?")
    
    #gets the html code for the valid games (games that match the entered name)
    correctGames = getCorrectGames(url, name)
    games =[]
    
    #if there are any valid games, put it in a list format
    if(correctGames):
        games = gameFormatter(correctGames)
        print(name,':')
        scores = []
        if(games):
            counter = 1
            
            #loop through the games and calculate the scores
            for game in games:
                score = calculateScores(game)
                scores.append(score)
                print('Game', counter, ':', score)
                counter+=1
            
            #print the average, strike percentage, and spare percentage
            print("Average:", avg(scores))
            calculateStats(games)
    
    #if there are no valid games for the entered name
    else:
        print('not a valid name')
