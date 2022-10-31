# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 09:31:40 2022

@author: hungd
"""

#%% Imports

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyautogui
import configparser
import argparse

import time
from copy import deepcopy

from mainChessAI import getBoard
from mainChessAI import letter_to_xpos
from mainChessAI import AIMove
from mainChessAI import AIHumanMove

#%% Arguments

def getArgs():
    # Parser
    parser = argparse.ArgumentParser()
    
    # Sleep Time
    parser.add_argument('--sleepTime',
                        type=int,
                        help='Time between click events',
                        default=3)
    
    # Sleep Time
    parser.add_argument('--numGames',
                        type=int,
                        help='Number of games to play', 
                        
                        default=1000)
    
    # Sleep Time
    parser.add_argument('--onlineOrComp',
                        type=str,
                        help='online or computer',
                        default='online')

    # Get arguments
    args = parser.parse_args()
    return args

#%% Import config

def importConfig(configFilePath):
    config = configparser.ConfigParser()
    config.read(configFilePath)
    return config

#%% Open Chrome Driver

def openChromeDriver():
    # Instantiate web driver
    driver = webdriver.Chrome()
    
    # Adding this here while the window is still the priority
    addKeyboardChromeExt(driver)
    return driver
    
#%% Add keyboard input chrome extension

def addKeyboardChromeExt(driver):
    # Maximize window
    driver.maximize_window()
    
    # Go to chess.com
    driver.get(r'https://chrome.google.com/webstore/detail/chesscom-keyboard/bghaancnengidpcefpkbbppinjmfnlhh?hl=en')
    
    # Add to Chrome button
    time.sleep(args.sleepTime)
    addButton = driver.find_element('xpath',
                                '/html/body/div[3]/div[2]/div/div/div[2]/div[2]/div/div/div/div')
    addButton.click()
    
    # Unfortunately have to use manual keyboard for this portion
    time.sleep(args.sleepTime)
    pyautogui.press('tab')
    pyautogui.press('enter')
    
#%% Play on chess.com

def logIn(driver, args, credentials):  
    # Add keyboard extension
    addKeyboardChromeExt(driver)
    
    # Go to chess.com
    driver.get(r'https://www.chess.com/')
    
    # Log in 
    time.sleep(args.sleepTime)
    logInButton = driver.find_element('xpath',
                                      '//*[@id="sb"]/div[3]/a[9]')
    logInButton.click()
    
    # Input username
    usernameField = driver.find_element('xpath', '//*[@id="username"]')
    usernameField.send_keys(credentials['chess.com']['username'])
    
    # Password
    passwordField = driver.find_element('xpath', '//*[@id="password"]')
    passwordField.send_keys(credentials['chess.com']['password'])
    
    # Log In again
    logInButton2 = driver.find_element('xpath',
                                      '//*[@id="login"]')
    logInButton2.click()

#%% New Game

def newGame(driver, args):
    if args.onlineOrComp == 'computer':
        playComputer(driver)
    else:
        playOnline(driver)
        
# Play computer
def playComputer(driver):
    # Go to play page
    time.sleep(args.sleepTime)
    driver.get(r'https://www.chess.com/play')
    
    # Play Computer
    time.sleep(args.sleepTime)
    playComputerButton = driver.find_element('xpath',
                                       '//*[@id="board-layout-sidebar"]/div/div[2]/div[1]/a[2]')
    playComputerButton.click()
    
    # click start
    time.sleep(args.sleepTime)
    if xpathExists(driver, '/html/body/div[26]/div[2]/div/div/button/div'):
        startButton = driver.find_element('xpath',
                                           '/html/body/div[26]/div[2]/div/div/button/div')
        startButton.click()
    
    # click start
    time.sleep(args.sleepTime)
    chooseButton = driver.find_element('xpath',
                                       '//*[@id="board-layout-sidebar"]/div/div[2]/button')
    chooseButton.click()
    
    # play button
    time.sleep(args.sleepTime)
    playButton = driver.find_element('xpath',
                                      '//*[@id="board-layout-sidebar"]/div/div[2]/button')
    playButton.click()
    
# Play Online
def playOnline(driver):
    # Go to play page
    time.sleep(args.sleepTime)
    driver.get(r'https://www.chess.com/play')
    
    # Play Online
    time.sleep(args.sleepTime)
    playOnlineButton = driver.find_element('xpath',
                                '//*[@id="board-layout-sidebar"]/div/div[2]/div[1]/a[1]/div[2]/div')
    playOnlineButton.click()
    
    # play button
    time.sleep(args.sleepTime)
    if xpathExists(driver, '//*[@id="board-layout-sidebar"]/div/div[2]/div/div[1]/div[1]/button'):
        playButton = driver.find_element('xpath',
                            '//*[@id="board-layout-sidebar"]/div/div[2]/div/div[1]/div[1]/button')
        playButton.click()

#%% Create path dictionary

def getPathDict():
    # Create Dict
    pathDict = {}
    pathDict['online'] = {}
    pathDict['computer'] = {}
    
    # Online
    pathDict['online']['colorIsWhite'] = (
        '//*[@id="move-list"]/vertical-move-list/div[1]/div[1]')
    pathDict['online']['isGG'] = (
        '//*[@id="board-layout-sidebar"]/div/div[2]/div[2]/div[1]/button[2]')
    pathDict['online']['playAsWhite'] = (
        '//*[@id="move-list"]/vertical-move-list/div[{}]/div[3]')
    pathDict['online']['playAsBlack'] = (
        '//*[@id="move-list"]/vertical-move-list/div[{}]/div[1]')
    pathDict['online']['myClock'] = '//*[@id="board-layout-player-bottom"]/div/div[4]/span'
    pathDict['online']['oppClock'] = '//*[@id="board-layout-player-top"]/div/div[4]/span'
    pathDict['online']['resign'] = (
        '//*[@id="board-layout-sidebar"]/div/div[2]/div[2]/div/div[1]/div[2]/span[2]')
    pathDict['online']['yesResign'] = (
        '//*[@id="board-layout-sidebar"]/div/div[2]/div[2]/div/div[1]/div[2]/div/button[2]')
    
    # Computer
    pathDict['computer']['colorIsWhite'] = (
        '//*[@id="board-layout-sidebar"]/div/vertical-move-list/div[1]/div[1]')
    pathDict['computer']['isGG'] = (
        '//*[@id="board-layout-sidebar"]/div/div[2]/div/div/div[4]/button[1]/span')
    pathDict['computer']['playAsWhite'] = (
        '//*[@id="board-layout-sidebar"]/div/vertical-move-list/div[{}]/div[2]')
    pathDict['computer']['playAsBlack'] = (
        '//*[@id="board-layout-sidebar"]/div/vertical-move-list/div[{}]/div[1]')
    pathDict['computer']['resign'] = (
        '//*[@id="board-layout-sidebar"]/div/div[2]/div[2]/div[2]/a')
    return pathDict   

#%% Play chess

def playChess(driver, pathDict, onlineOrComp = 'computer'):
    # Wait for game to start
    if onlineOrComp == 'online':
        if not foundGame(driver, pathDict, onlineOrComp):
            return
         
    if colorIsWhite(driver, pathDict, onlineOrComp):
        playAsWhite(driver, pathDict, onlineOrComp)
    else:
        playAsBlack(driver, pathDict, onlineOrComp)

# Searching for game
def foundGame(driver, pathDict, onlineOrComp):
    maxSecondsToSearch = 0
    while True:
        time.sleep(1)
        print('Searching for game...')
        maxSecondsToSearch += 1
        
        # Over limit
        if maxSecondsToSearch > 30:
            return False

        # If clock exists, game has started
        if xpathExists(driver, pathDict['online']['myClock']):
            return True
   
# Determine if we are white or black
def colorIsWhite(driver, pathDict, onlineOrComp):
    # Wait for clocks to start
    if onlineOrComp == 'online':
        while True:
            time.sleep(2)
            if (':00' not in driver.find_element('xpath', pathDict[onlineOrComp]['myClock']).text or 
                ':00' not in driver.find_element('xpath', pathDict[onlineOrComp]['oppClock']).text):
                break
    
    # Check to see if opponent made a move
    xpath = pathDict[onlineOrComp]['colorIsWhite']
    if xpathExists(driver, xpath):
        return False
    return True

#%% Check for checkmate

def isGG(driver, pathDict, onlineOrComp):
    # Opponent xpath
    xpath_gg = pathDict[onlineOrComp]['isGG']
    if xpathExists(driver, xpath_gg):
        return True
    return False

#%% Check if element exists

def xpathExists(driver, xpath):
    try:
        driver.find_element('xpath', xpath)
    except:
        return False
    return True
        
#%% Resign Game

def resignGame(driver, xpath, pathDict, onlineOrComp, position):
    # En passant or they promote
    if xpathExists(driver, '{}/div'.format(xpath)) or '=' in position:
        chooseButton = driver.find_element('xpath',
                                           pathDict[onlineOrComp]['resign'])
        chooseButton.click()
        
        if onlineOrComp == 'online':
            chooseButton = driver.find_element('xpath',
                                               pathDict['online']['yesResign'])
            chooseButton.click()
        return True
    return False
    
#%% Play as white

def playAsWhite(driver, pathDict, onlineOrComp):
    # Show initial board position
    board = getBoard()
    
    # AI Makes first move
    board, ai_xfrom, ai_yfrom, ai_xto, ai_yto = AIMove(board)
    ai_move = transformAIMove(ai_xfrom, ai_yfrom, ai_xto, ai_yto)
    ai_move = convertMoveFromBlackToWhite(ai_move)
    
    # Input move in chess.com
    moveInput = driver.find_element('xpath', '//*[@id="ccHelper-input"]')
    moveInput.send_keys(ai_move)
    moveInput.send_keys(Keys.ENTER)
    
    # Start move num at 1 then inc by 2 to get white moves
    moveNum = 1
    while True:
        # Define move
        xpath = pathDict[onlineOrComp]['playAsWhite'].format(moveNum)
        
        # Check if move exists
        if not xpathExists(driver, xpath):
            # GG
            if isGG(driver, pathDict, onlineOrComp):
                break
            
            time.sleep(.25)
            continue
        
        # Prev Board Position
        boardPrev = deepcopy(board)
        
        # Get position and piece
        position, piece, prevFile, prevRank = getPositionPiece(xpath)
        
        # GG
        if isGG(driver, pathDict, onlineOrComp):
            break
        
        # Checkmate
        if '#' in position:
            break
        
        # En passant
        if resignGame(driver, xpath, pathDict, onlineOrComp, position):
            break
            
        # Convert position to black
        position, prevRank = convertMoveFromWhiteToBlack(position, prevRank)
        
        # New move
        opponentMove = getOpponentMove(boardPrev, position, piece, prevFile, prevRank)
        
        # Get AI move
        board, ai_move = getAImove(board, opponentMove)
        
        # Check for queen Promotion
        ai_move = queenPromotion(ai_move, boardPrev)
        
        # Convert from black to white
        ai_move = convertMoveFromBlackToWhite(ai_move)
        
        # Input move in chess.com
        moveInput = driver.find_element('xpath', '//*[@id="ccHelper-input"]')
        moveInput.send_keys(ai_move)
        moveInput.send_keys(Keys.ENTER)
                
        # Increment move number
        moveNum += 1
        
# Convert from white to black
def convertMoveFromBlackToWhite(ai_move):
    # Check for takes queen promotion
    if 'x' in ai_move and '=Q' in ai_move:
        digit = 8 - int(ai_move[3]) + 1
        return '{}{}{}'.format(ai_move[:3], digit, ai_move[4:])
    
    # Check if standard queen promotion
    if '=Q' in ai_move:
        digit = 8 - int(ai_move[1]) + 1
        return '{}{}{}'.format(ai_move[0], digit, ai_move[2:])
      
    # Regular non-queen promotion moves
    digit1 = 8 - int(ai_move[1]) + 1
    digit2 = 8 - int(ai_move[3]) + 1
    return '{}{}{}{}'.format(ai_move[0], digit1, ai_move[2], digit2)

# Convert from white to black
def convertMoveFromWhiteToBlack(position, prevRank):
    if 'O-O' in position:
        return position, prevRank
    
    # Position
    digit = 8 - int(position[1]) + 1
    position = '{}{}'.format(position[0], digit)
    
    # prevRank
    if prevRank is not None:
        prevRank = 8 - prevRank + 1
    return position, prevRank
    
#%% Play as black

def playAsBlack(driver, pathDict, onlineOrComp):
    # Show initial board position
    board = getBoard()
    
    # Start move num at 1 then inc by 2 to get white moves
    moveNum = 1
    while True:
        # Define move
        xpath = pathDict[onlineOrComp]['playAsBlack'].format(moveNum)
        
        # Check if move exists
        if not xpathExists(driver, xpath):
            # GG
            if isGG(driver, pathDict, onlineOrComp):
                return
            
            time.sleep(.25)
            continue
        
        # Prev Board Position
        boardPrev = deepcopy(board)
        
        # Get position and piece
        position, piece, prevFile, prevRank = getPositionPiece(xpath)
        
        # GG
        if isGG(driver, pathDict, onlineOrComp):
            return
        
        # Checkmate
        if '#' in position:
            break
        
        # En passant or if they get a promoted pawn
        if resignGame(driver, xpath, pathDict, onlineOrComp, position):
            break
        
        # New move
        opponentMove = getOpponentMove(boardPrev, position, piece, prevFile, prevRank)
        
        # Get AI move
        board, ai_move = getAImove(board, opponentMove)
        
        # Check for queen promotion
        ai_move = queenPromotion(ai_move, boardPrev)
        
        # Input move in chess.com
        moveInput = driver.find_element('xpath', '//*[@id="ccHelper-input"]')
        moveInput.send_keys(ai_move)
        moveInput.send_keys(Keys.ENTER)
                
        # Increment move number
        moveNum += 1
 
#%% Queen promotion

def queenPromotion(ai_move, boardPrev):
    # Separate before and after position
    position1 = ai_move[:2]
    position2 = ai_move[2:]
    
    # get x y positions
    xpos1, ypos1 = convertPosToxy(position1)
    xpos2, ypos2 = convertPosToxy(position2)
    
    # Return if move is not from 6 -> 7 or 1-> 0
    if not ((ypos1 == 6 and ypos2 == 7) or (ypos1 == 1 and ypos2 == 0)):
        return ai_move
    
    # Verify original piece was a pawn
    if boardPrev.chesspieces[xpos1][ypos1].PIECE_TYPE != 'P':
        return ai_move
    
    # If a standard move forward promotion
    if xpos1 == xpos2:
        ai_move = '{}=Q'.format(position2)
        return ai_move
    
    # If the pawn takes a piece
    if xpos1 != xpos2:
        ai_move = '{}x{}=Q'.format(position1[0], position2)
        return ai_move

#%% Get position and piece

def getPositionPiece(xpath, prevRank=None, prevFile=None):
    # Get position
    position = driver.find_element('xpath', xpath).text
    
    # If castles
    if 'O-O' in position:
        return position, '', prevFile, prevRank
    
    # Remove 'x' from position
    position = position.replace('x', '')
    
    # Remove '+' from position
    position = position.replace('+', '')
    
    # Get previous rank
    if len(position) == 3:
        try:
            prevRank = int(position[0])
        except:
            prevFile = position[0]
        position = position[1:]
    
    if not xpathExists(driver, xpath + '/span'):
        return position, 'P', prevFile, prevRank
    
    # Piece
    piece = driver.find_element('xpath', xpath + '/span').get_attribute('data-figurine')
    return position, piece, prevFile, prevRank

#%% Find Previous position

def getOpponentMove(boardPrev, position, piece, prevFile, prevRank):
    # Castle King Side
    if position == 'O-O':
        return position
    
    # Castle Queen Side
    if position == 'O-O-O':
        return position
    
    # Get x-y position
    xpos, ypos = convertPosToxy(position)
    
    # Get previous rank and file if applicable
    prevFile_xpos, prevRank_ypos = None, None
    if prevFile is not None:
        prevFile_xpos = letter_to_xpos(prevFile)
    if prevRank is not None:
        prevRank_ypos = 8 - prevRank
    
    # Get prev x y coordinate
    xprev, yprev = getPrevXYCoord(boardPrev, xpos, ypos, piece, prevFile, prevRank,
                                  prevFile_xpos, prevRank_ypos)
    
    # Convert xprev, yprev to string
    file = xposToLetter(xprev)
    rank = yposToNumber(yprev)
    
    # Get full move
    move = '{}{} {}'.format(file, rank, position)
    return move
    
# Get prev x y coordinate
def getPrevXYCoord(boardPrev, xpos, ypos, piece, prevFile, prevRank,
                              prevFile_xpos, prevRank_ypos):    
    # Get Previous position
    for file in range(len(boardPrev.chesspieces)):
        for rank in range(len(boardPrev.chesspieces[file])):
            # Check if empty space
            if boardPrev.chesspieces[file][rank] == 0:
                continue
            
            # Check if piece is the same
            if boardPrev.chesspieces[file][rank].PIECE_TYPE != piece:
                continue
            
            # Check if correct color
            if boardPrev.chesspieces[file][rank].color != 'W':  # Always white
                continue
            
            # Check for correct file
            # if prevFile is not None and prevFile_xpos != file:
            #     continue
            
            # Check for correct rank
            # if prevRank is not None and prevRank_ypos != rank:
            #     continue
            
            # Get possible moves
            possibleMoves = boardPrev.chesspieces[file][rank].get_possible_moves(boardPrev)
            
            # Continue if no possible moves for this piece
            if not possibleMoves:
                continue
            
            for i in range(len(possibleMoves)):
                if xpos == possibleMoves[i].xto and ypos == possibleMoves[i].yto:
                    xprev, yprev = possibleMoves[i].xfrom, possibleMoves[i].yfrom
                    return xprev, yprev
            
# Convert position to x-y
def convertPosToxy(position):
    # Convert postion to x-y coordinates
    xpos = letter_to_xpos(position[0])
    ypos = 8 - int(position[1])
    return xpos, ypos

# Convert xpos to letter
def xposToLetter(xpos):
    if xpos == 0:
        return 'a'
    if xpos == 1:
        return 'b'
    if xpos == 2:
        return 'c'
    if xpos == 3:
        return 'd'
    if xpos == 4:
        return 'e'
    if xpos == 5:
        return 'f'
    if xpos == 6:
        return 'g'
    if xpos == 7:
        return 'h'
    
# Convert ypos to number
def yposToNumber(ypos):
    return str(8 - int(ypos))
     
#%% Get AI move

def getAImove(board, opponentMove):
    # Get AI move
    board, ai_xfrom, ai_yfrom, ai_xto, ai_yto = AIHumanMove(board, move_str=opponentMove)
    ai_move = transformAIMove(ai_xfrom, ai_yfrom, ai_xto, ai_yto)
    return board, ai_move

def transformAIMove(ai_xfrom, ai_yfrom, ai_xto, ai_yto):
    ai_xfrom = xposToLetter(ai_xfrom)
    ai_yfrom = yposToNumber(ai_yfrom)
    ai_xto = xposToLetter(ai_xto)
    ai_yto = yposToNumber(ai_yto)
    ai_move = '{}{}{}{}'.format(ai_xfrom, ai_yfrom, ai_xto, ai_yto)
    return ai_move

#%% Play multiple games

def playMultipleGames(driver, pathDict, args):
    for i in range(args.numGames):
        # New Game
        print('Game Number: {}'.format(i+1))
        newGame(driver, args)
        
        # Make moves
        playChess(driver, pathDict, onlineOrComp=args.onlineOrComp)
        
#%% Main

if __name__ == '__main__':
    # Get Arguments
    args = getArgs()
    
    # Credentials
    credentials = importConfig(configFilePath='credentials/config.ini')
    
    # Open chrome driver and get chrome extension
    driver = openChromeDriver()
    
    # Log in
    logIn(driver, args, credentials)
    
    # Get path dictionary
    pathDict = getPathDict()
    
    # Play Games
    playMultipleGames(driver, pathDict, args)
    
    driver.close()
    
    
    
    
