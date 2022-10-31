# chessAI
Chess AI that can play on chess.com

*** This is just a fun programming poject and the intention is not to gain ELO points on chess.com. ***

# Set up
- Install requirements
  - pip install -r requirements.txt
- Place chess.com login information in config.ini file
  - use config_template.ini as a template but rename the file to config.ini

# Arguments
- onlineOrComp - Choose if you want to play the chess.com computer or play real people online
- numGames - Choose how many games you would like the AI to play
- sleepTime - Defaulted to 2 seconds.  This is the time between click events while logging into chess.com

# How to run
- Pip install the requirements.txt file
  - pip install -r requirements.txt
- Add config.ini to credentials folder with your chess.com credentials
  - Use template but rename to config.ini
- Play against the computer on chess.com
  - main.py --onlineOrComp computer --numGames 2 --sleepTime 2
  
- Play live chess
  - main.py --onlineOrComp online --numGames 2 --sleepTime 2
  
# Limitations

- AI is about ~1200 ELO 
- Will automatically resign if opponent does En Passant or promotes a piece from a pawn
- AI promotions will always be to a queen
- Opponent may castle but AI does not know how to castle
