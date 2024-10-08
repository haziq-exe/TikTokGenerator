import praw
import re
import sys
import os
from dotenv import load_dotenv
load_dotenv()

#Removed replacement_dict, it is essentially a hand-made dictionary that changes certain swearwords

client_id = os.environ['REDDIT_CLIENTID']
client_secret = os.environ['REDDIT_CLIENT_SECRET']
user_agent = os.environ['REDDIT_USER']


reddit = praw.Reddit(
    client_id= client_id,
    client_secret= client_secret,
    user_agent=user_agent
)

done_URLS = []


def remove_after_word(text, word):
    
    lower_text = text.lower()
    lower_word = word.lower()

    
    if lower_word in lower_text:
     
        split_index = lower_text.index(lower_word)
        return text[:split_index].strip()
    else:
     
        return text
    
def split_into_chunks(input_string, chunk_size=15000): #Can be used to split into parts, however currently doesnt cause 15000 too big chunk size
    words = input_string.split()
    chunks = []
    current_chunk = ""
    
    for word in words:
        
        if len(current_chunk) + len(word) + 1 > chunk_size:
            chunks.append(current_chunk)
            current_chunk = word
        else:
            if current_chunk:
                current_chunk += " " + word
            else:
                current_chunk = word
    
    
    if current_chunk:
        if len(current_chunk) < 500:
            chunks[len(chunks) - 1] = chunks[len(chunks) - 1] + " " + current_chunk
        else:
            chunks.append(current_chunk)
    
    return chunks

def remove_links(text):
    # Regex pattern to match URLs
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    # Substitute URLs with an empty string
    return re.sub(url_pattern, '', text)


def replace_integer_with_dot(text):
    
    pattern = r'(\d+)\s*([FfMm])'  
    
    def replacement(match):
        return f"{match.group(1)}.{match.group(2).upper()}"

    modified_text = re.sub(pattern, replacement, text)
    
    return modified_text

def replace_words(text, replacements): 
    def replace(match):
        
        word = match.group(0)
        
        replacement = replacements[match.group(0).lower()]
        
        if word.isupper():
            return replacement.upper()
        elif word[0].isupper():
            return replacement.capitalize()
        else:
            return replacement
    
    exclude_boundary = r"\\'"
    
    boundary_keys = [key for key in replacements.keys() if key != exclude_boundary]
    boundary_pattern = r'\b(' + '|'.join(re.escape(key) for key in boundary_keys) + r')\b'

   
    if exclude_boundary:
        non_boundary_pattern = re.escape(exclude_boundary)
        pattern = re.compile(boundary_pattern + '|' + non_boundary_pattern, re.IGNORECASE)
    else:
        pattern = re.compile(boundary_pattern, re.IGNORECASE)



    
    return pattern.sub(replace, text)

def fetch(total_posts, subreddit=['AmITheAsshole'], time='year', url_file=None):

    Title = []
    Final_Titles = []
    Posttemp = []
    Post = []
    Subreddit = []
    fetched_posts = 0
    count = 0
    with open("/Users/haziq/Desktop/TikTokGenerator/RedditTypeVideo/PostManagement/CompletedPosts.txt", 'r') as done_file:
        check_url = set(line.strip() for line in done_file)
        done_file.close()

    # if url_file == None:
    # subreddit1 = reddit.subreddit(subreddit)

    for sub in subreddit:
        fetched_posts = 0
        while fetched_posts < total_posts:
            subreddit1 = reddit.subreddit(sub)
            submissions = subreddit1.top(time_filter=time, limit = count + 1)
            for submission in submissions:
                if 'UPDATE' in submission.title or 'update' in submission.title or len(submission.selftext) > 5000 or submission.url in check_url or len(submission.title) > len(submission.selftext) or len(submission.selftext) < 500:
                    count += 1
                    continue
                else:
                    Posttemp.append(submission)

                    fetched_posts += 1
                    count += 1

    highestupvote = [0] * total_posts
    topposts = [None] * total_posts
    for submission in Posttemp:
        if any(submission.score > upvote for upvote in highestupvote):
            topposts[total_posts - 1] = submission
            highestupvote[total_posts - 1] = submission.score
            topposts.sort(reverse=True)
            highestupvote.sort(reverse=True)

    for post in topposts:
        Title.append(post.title)
        Post.append(post.selftext)
        Subreddit.append(str(post.subreddit))
        print(post.url)
        Post[0] = remove_after_word(text = Post[0], word='edit:')
        if len(Post[0]) > 2300:
            Part = split_into_chunks(Post[0])  
        else:
            Part = [Post[0]]
        with open("/Users/haziq/Desktop/TikTokGenerator/RedditTypeVideo/PostManagement/CompletedPosts.txt", 'a') as done_file:
            done_file.write(f'{post.url}\n')
                
    # else: FOLLOWING CODE IS REDUNDANT, IT TAKES URLs IN FROM A .txt FILE THAT HAD REDDIT POSTS ON IT I HAND PICKED
    #     with open("/Users/haziq/Desktop/TikTokGenerator/PostManagement/CompletedPosts.txt", 'r') as done_file:
    #         check_url = set(line.strip() for line in done_file)
    #         done_file.close()

    #     with open(url_file, 'r') as file:
    #         while fetched_posts < total_posts:
    #                 url = file.readline().strip()
    #                 if url == "":
    #                     sys.exit("No more URLs in file")
    #                 url_slice = url[24:]
    #                 slash_index = url_slice.find('/')
    #                 subreddit = url_slice[:slash_index]
    #                 index_ID = 40 + len(subreddit)
    #                 if url in check_url:
    #                     continue
    #                 else:
    #                     post_ID_slice = url[index_ID:]
    #                     slash_index = post_ID_slice.find('/')
    #                     post_ID = post_ID_slice[:slash_index]
    #                     submission_post = reddit.submission(id=post_ID)
    #                     if 'UPDATE' in submission_post.title or 'update' in submission_post.title:
    #                         continue
    #                     else:
    #                         if 'AITA?' in (submission_post.selftext.lower()):
    #                             position = submission_post.selftext.find("AITA?")
    #                             post_text = (submission_post.selftext[:position + len("AITA?")])
                            
    #                         if (len(post_text) + len(submission_post.title) >= 3000):
    #                             continue
    #                         else:
    #                             print(f'Post length: {(len(post_text) + len(submission_post.title))}')
    #                             Title.append(submission_post.title)
    #                             Post.append(post_text)
    #                             with open("/Users/haziq/Desktop/TikTokGenerator/PostManagement/CompletedPosts.txt", 'a') as done_file:
    #                                 done_file.write(f'{url}\n')
    #                             fetched_posts += 1
    #                             print(f'{fetched_posts} / {total_posts}    Fetched')
                
    # for title, post in zip(Title, Post):
    #     new_title = replace_words(title, replacement_dict)
    #     new_post = replace_words(post, replacement_dict)
    #     post_edit = replace_integer_with_dot(new_post)
    #     edit_title = replace_integer_with_dot(new_title)
    #     final_title = remove_links(edit_title)
    #     final_post = remove_links(post_edit)
    new_title = replace_words(Title[0], replacement_dict)
    edit_title = replace_integer_with_dot(new_title)
    final_title = remove_links(edit_title)
    for i in range(len(Part)):
        Part[i] = replace_words(Part[i], replacement_dict)
        Part[i] = replace_integer_with_dot(Part[i])
        Part[i] = remove_links(Part[i])

        Final_Titles.append(final_title)
        # Script.append(f'{final_title} :_: {final_post}')


    return Part, Final_Titles, Subreddit
    
