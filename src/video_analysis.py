import whisper
import librosa
import cv2
import numpy as np
from deepface import DeepFace
import json
from pathlib import Path


# load the model once at the top of the file
model = whisper.load_model("base")

def transcribe_audio(video_path):
    video_path = str(video_path)  # ✅ Convert Path object to string
    result = model.transcribe(video_path)
    return result["text"]


def analyze_speech_features(video_path):
    y, sr = librosa.load(video_path, sr=None)
    duration = librosa.get_duration(y=y, sr=sr)
    words = len(transcribe_audio(video_path).split())
    speech_rate = round(words / duration * 60, 2)  # words per minute
    return {"speech_rate_wpm": speech_rate, "duration_sec": duration}


def analyze_facial_emotions(video_path):
    cap = cv2.VideoCapture(video_path)
    emotions = {"happy": 0, "sad": 0, "angry": 0, "surprise": 0, "neutral": 0}
    frames = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        try:
            analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            dominant = analysis['dominant_emotion']
            if dominant in emotions:
                emotions[dominant] += 1
        except:
            pass
        frames += 1
    cap.release()
    # Convert counts to percentages
    for k in emotions:
        emotions[k] = round(emotions[k] / frames * 100, 2) if frames > 0 else 0
    return emotions


def analyze_video(video_path):
    transcript = transcribe_audio(video_path)
    speech_features = analyze_speech_features(video_path)
    facial_emotions = analyze_facial_emotions(video_path)

    return {
        "transcript": transcript,
        "speech_features": speech_features,
        "facial_emotions": facial_emotions
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Analyze candidate video pitch")
    parser.add_argument("video_path", type=str, help="Path to candidate video (mp4)")
    args = parser.parse_args()

    result = analyze_video(args.video_path)

    output_path = Path(args.video_path).with_suffix(".json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    print(f"✅ Video analysis saved to {output_path}")
