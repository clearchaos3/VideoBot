# -*- coding: UTF-8 -*-
import requests
from gtts import gTTS
from gtts.tokenizer import pre_processors
import gtts.tokenizer.symbols
from PIL import Image, ImageDraw, ImageFont
import os
import wget
from moviepy.editor import *
from dotenv import load_dotenv

load_dotenv()
username = os.getenv('username')
password = os.getenv('password')
token = os.getenv('token')
token_secret = os.getenv('token_secret')

base_url = 'https://www.reddit.com/'
subreddit = 'pics'
data = {'grant_type': 'password', 'username': username, 'password': password}
auth = requests.auth.HTTPBasicAuth(token, token_secret)
r = requests.post(base_url + 'api/v1/access_token',
                  data=data,
                  headers={'user-agent': 'Posts by supleezy'},
                  auth=auth)
d = r.json()
token = 'bearer ' + d['access_token']
base_url = 'https://oauth.reddit.com'
headers = {'Authorization': token, 'User-Agent': 'VideoBot by Supleezy'}
response = requests.get(base_url + '/api/v1/me', headers=headers)
payload = {'t': 'hour', 'limit': 5}
r = requests.get(base_url + '/r/' + subreddit + '/top', headers=headers, params=payload)
js = r.json()
# durationText = ''
# mp3List = ''
#
# gtts.tokenizer.symbols.SUB_PAIRS.append(('&amp;', 'and'))

for i in range(js['data']['dist']):
    print('Starting post ' + str(i+1))
    title = js['data']['children'][i]['data']['title']
    title = pre_processors.word_sub(title)
    thumbnail = js['data']['children'][i]['data']['url']
    if("imgur" in thumbnail):
        break
    print('Downloading Image 👨‍💻')
    local_image_filename = wget.download(thumbnail)
    print('Creating Image 🖼')
    postImage = Image.open(local_image_filename)
    img_w, img_h = postImage.size
    if (img_w > 1500) or (img_h > 1500):
        print('img_w: ' + str(img_w) + ' --- img_h: ' + str(img_h))
        postImage.thumbnail((1500, 1500))
        postImage.save(local_image_filename)
        print('new size: ' + str(postImage.size))
        img_w, img_h = (postImage.size)

    bg_w = img_w
    bg_h = img_h * 1.2
    bg = Image.new('RGB', (int(bg_w), int(bg_h)))
    print('bg.size: ' + str(bg.size))

    offset = (0, int(bg_h - img_h))

    print(offset)

    bg.paste(postImage, offset)
    print('new bg.size: ' + str(bg.size))
    d = ImageDraw.Draw(bg)
    fnt = ImageFont.truetype('/Library/Fonts/SF-Pro-Display-Thin.otf', 72)
    d.text((0, 0), 'title goes here', font=fnt, fill=(255, 255, 255))
    local_image_filename = 'Image' + str(i).zfill(3) + '.png'
    bg.save(str(local_image_filename))

#
# bgClip = VideoFileClip('woods.mp4')
# overlayClip = VideoFileClip('pic.mp4')

# overlayPic = 'test.jpg'
# overlayClips = []
#
# for i in range(32):
#     overlayClips.append(ImageClip(overlayPic).set_duration(1))
#
# print(overlayClips)
# video = concatenate(overlayClips, method="compose")
# video.write_videofile('pic.mp4', fps=24)

#
# bgClip_w, bgClip_h = 1920, 1080
# overlayClip_w, overlayClip_h = 960, 720
#
# x, y = (bgClip_w-overlayClip_w)/2, (bgClip_h-overlayClip_h)/2
#
# video = CompositeVideoClip([bgClip, overlayClip.set_position((x, y))], size=(1920, 1080))
#
# video.write_videofile('moviepyOutput.mp4')




# durationText = durationText + "file '/Users/ryanlee/PycharmProjects/VideoBot/" + local_image_filename + "'\n"
# finalDurationText = "file '/Users/ryanlee/PycharmProjects/VideoBot/" + local_image_filename + "'"

    # print('Creating title mp3 💿')
    # ttsTitle = gTTS(title)
    # mp3Title = 'Title' + str(i).zfill(3) + '.mp3'
    # titleOriginal = mp3Title
    # mp3Title = "file '" + mp3Title
    # mp3List = mp3List + mp3Title + '\n'
    # ttsTitle.save(titleOriginal)
    # ffprobe = 'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 Title' + str(i).zfill(3) + '.mp3'
    # duration = os.popen(ffprobe).read().replace('duration=', '')
    # durationText = durationText + 'duration ' + str(duration) + '\n'
    #
    # print('Post ' + str(i+1) + ' complete! ✅')

# print('Creating text files 📝')
# durationText = durationText + finalDurationText
# durationFile = open('duration.txt', 'w')
# durationFile.write(durationText)
# durationFile.close()
# mp3File = open('mp3File.txt', 'w')
# mp3File.write(mp3List)
# mp3File.close()
# print('Creating final audio file 🔊')
# mp3Command = 'ffmpeg -f concat -i mp3File.txt -c copy -loglevel panic output.mp3'
# os.system(mp3Command)
# print('Creating slideshow 📼')
# ffmpeg = 'ffmpeg -f concat -safe 0 -i duration.txt -vsync vfr -framerate 24 -pix_fmt yuv420p -loglevel panic ' + subreddit + '.mp4'
# os.system(ffmpeg)
# print('Creating final video 🔥')
# final = 'ffmpeg -i ' + subreddit + '.mp4 -i output.mp3 -c:v copy -c:a aac -strict experimental -loglevel panic ' + subreddit + 'FINAL.mp4'
# os.system(final)
# print('✨' + subreddit + 'FINAL.mp4 CREATED SUCCESSFULLY✨')
#
# print('Cleaning Up 🧹💨')
# ls = os.popen('ls').read()
# ls = ls.split('\n')
# ls.remove('VideoBot.py')
# ls.remove('bg.jpg')
# ls.remove('venv')
# ls.remove('picsFINAL.mp4')
# ls.remove('README.md')
# ls.remove('')
# for line in ls:
#     cmd = 'rm ' + line
#     os.system(cmd)
