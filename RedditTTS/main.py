from VideoGeneration import Subreddit_Video
import random
from datetime import datetime
random.seed(datetime.now().timestamp())

#Vids:
#'RL', 'Powerwash', 'Ski', 'BikeFPS', 'GTA', 'MC', 'ClashRoyale', 'Cooking', 'Horror', 'Horror2'

#Prompts:
#"WritingPrompt", "Drugs", "RageBait", "WorkIssue", "TragicLover", "TragicManhood", "LostTeenageBoy", "DifferentMemory", 
# "DudeUplifting", "LongDistance", "FamilySecret", "LetsNotMeetPrompt", "HorrorPrompt, "r/NoSleep"

#Some Subreddits:
#relationship_advice, tifu, AmITheAsshole

n = 2 #random.randint(1, 10)
weeknum = 1
usual_subreddits = ['relationship_advice', 'AmITheAsshole', 'tifu']
banger_find = ['confessions']

if n == 10:
    Subreddit_Video(weeknumber=weeknum, numberofposts=1, Vid=None, speaker="Liv", prompttype=['r/NoSleep'], subreddit=None, time=None)
else:    
    Subreddit_Video(weeknumber=weeknum, numberofposts=1, Vid=None, speaker="Scarlett", prompttype=None, subreddit=banger_find, time='all', sound='Very Sad', sound_vol='background')
