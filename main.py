import praw
from openai import OpenAI
from reddit import *
from convert_to_audio import voice
import whisper
from datetime import timedelta
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from transcribe import *
from add_title import *
from combine import *
from video import add_subtitles
import random
from clear import *
from trans import transcribe_1

subreddit_list = ['entitledpeople']

subreddit = subreddit_list[random.randint(0,len(subreddit_list) - 1)]
stories = find_top(subreddit, filter='week')
chosen_index = random.randint(0,9)
stories_list = list(stories.items())
chosen_title, chosen_text = stories_list[chosen_index]
print(chosen_title, chosen_text)
voice(chosen_text)
transcribe_1()
add_title_and_shift_subtitles('r/' + subreddit + '\n' + '\n' + '\n' + chosen_title)
combine()
add_subtitles()
clear_multiple(file1='src/audio_with_silence.mp3', 
              file2='src/output_video_with_audio.mp4', file3='src/audio.mp3', 
              file4='src/trim_vid.mp4', file5='temp_silence.wav', file6='src/subtitles.srt')


    
