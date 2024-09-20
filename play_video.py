import os
import json
import cv2
import re
from moviepy.editor import VideoFileClip, concatenate_videoclips

with open('palabras.json') as f:
    palabra_a_video = json.load(f)
    
with open('palabras_ignoradas.json') as f:
    ignorar = json.load(f)

def sanitize_palabra(palabra):
    return palabra.replace("¿", "").replace("¡", "").replace("!", "").replace('"', "").replace("'", "")

def buscar_video_por_palabra(palabra):
    palabra = palabra.lower()
    for key, value in palabra_a_video.items():
        keys = [k.strip().lower() for k in key.split(",")]
        if palabra in keys:
            return os.path.join('videos', value)
    return None

def tomar_video(palabra):
    palabra = sanitize_palabra(palabra)

    video_file = buscar_video_por_palabra(palabra)
    if video_file:
        return video_file

    videos_letras = []
    for letra in palabra:
        if letra.isalnum():
            video_letra = buscar_video_por_palabra(letra)
            if video_letra:
                videos_letras.append(video_letra)

    return videos_letras if videos_letras else None

def concatenate_videos(video_files, output_filename="concatena2.mp4"):
    clips = []
    for video_file in video_files:
        if not os.path.exists(video_file):
            print(f"Video not found: {video_file}")
            continue  

        clips.append(VideoFileClip(video_file))

    if clips:
        final_clip = concatenate_videoclips(clips)
        final_clip.write_videofile(output_filename)
        display_video(output_filename)

def display_video(filename):
    cap = cv2.VideoCapture(filename)
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
        if palabra.lower() in ignorar:
            continue
        video_file = tomar_video(palabra)
        if video_file:
            if isinstance(video_file, list):
                video_files.extend(video_file)
            else:
                video_files.append(video_file)

    if video_files:
        concatenate_videos(video_files)