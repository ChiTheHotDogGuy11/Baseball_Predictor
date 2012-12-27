This program can only run on windows due to the usage of winsound.

To Run:
Open gameMenu.py and run the file.


Summary:

Our project is a predictive model for the outcome of baseball games with an interactive user interface. The main purpose of the project is to let one or two users choose a team of baseball players from the MLB and pit them against another team of chosen players in order to see the outcome of the game. The user will essentially assume the role of coach, making tactical decisions to try and improve their team’s chances of winning the game. Our project is comprised of two major parts: the predictive algorithm and the user interface.

	Our predictive algorithm begins with basic player data. We will web scrape all of the data we need from www.baseball-reference.com and save the data for each player in a separate file. The model we use will focus solely on a pitcher vs. batter matchup. That is, instead of trying to predict what will happen on a pitch- by- pitch basis, we will instead focus on what the overall outcome of the at bat is. We will use various statistics about each player to evaluate the likelihood that the batter will reach base.  
