import sys
import os
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(parent_directory, 'RedditTypeVideo'))
import ImageGen
from CommentFetch import load_comments

num_comments = 20

Question, Comments = load_comments(numofcomments=num_comments)

Question = Question[0]

Run_Number = 6

ImageGen.create_SlideShowpost(Question=Question, gennumber=Run_Number)

for i in range(len(Comments)):
    ImageGen.create_comment(Comments[i], gennumber=Run_Number, slidenumber=(i+1))
