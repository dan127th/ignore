import os
import json
import cv2
import re
from moviepy.editor import VideoFileClip, concatenate_videoclips


with open('palabras.json') as f:
    palabra_a_video = json.load(f)

def tomar_video(palabra):
    palabra = palabra.replace("¿", "").replace("¡", "").replace("!", "").replace('"', "").replace("'", "")  # remove unwanted symbols

    for key, value in palabra_a_video.items():
        keys = [k.strip().lower() for k in key.split(",")]
        if palabra.lower() in keys:
            video_file = value
            break
    else:
        video_file = None

    if video_file:
        video_file_path = os.path.join('videos', video_file)
        return video_file_path
    else:
        videos_letras = []
        for letra in palabra.lower():
            if letra.isalnum():  # only recurse for alphanumeric characters
                video_letra = tomar_video(letra)
                if video_letra:
                    videos_letras.append(video_letra)
        if videos_letras:
            return videos_letras
        else:
            return None
    
def concatenate_videos(video_files):
    clips = []

    for video_file in video_files:
        if not os.path.exists(video_file):
            print(f"Video NO encontrado: {video_file}")
            return
        clip = VideoFileClip(video_file)
        clips.append(clip)

    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile("concatena2.mp4")

    cap = cv2.VideoCapture("concatena2.mp4")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Video', frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def play_videos(words):
    words = re.findall(r"[\w\.]+", words)  
    video_files = []

    for palabra in words:
        video_file = tomar_video(palabra)
        if video_file:
            if isinstance(video_file, list):
                video_files.extend(video_file)
            else:
                video_files.append(video_file)

    if video_files:
        concatenate_videos(video_files)