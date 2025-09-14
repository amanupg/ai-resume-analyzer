import sys

try:
    import fitz        # PyMuPDF
    import spacy
    import sentence_transformers
    import torch
    import librosa
    import whisper
    import mediapipe
    import deepface
    import streamlit
    print("Core imports OK")
except Exception as e:
    print("Import error:", e)
    sys.exit(1)
