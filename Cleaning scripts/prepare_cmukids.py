import os
import re
import string
import subprocess
import random
import shutil
from tqdm import tqdm

DATA_DIR   = "input"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_transcript(trn_path):
    with open(trn_path, "r", encoding="utf-8") as f:
        text = f.read()
    # join multiple lines
    text = text.replace("\n", " ")
    # remove bracketed tags [...]
    text = re.sub(r'\[.*?\]', '', text)
    # remove phonetic annotations /.../ 
    text = re.sub(r'/[^/]+/', '', text)
    # remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # collapse whitespace
    text = re.sub(r' +', ' ', text).strip()
    return text.lower()

skipped_empty   = 0
skipped_no_trn  = 0
processed       = 0

for speaker in tqdm(os.listdir(DATA_DIR)):
    signal_dir = os.path.join(DATA_DIR, speaker, "signal")
    trans_dir  = os.path.join(DATA_DIR, speaker, "trans")

    if not os.path.isdir(signal_dir) or not os.path.isdir(trans_dir):
        continue

    for sph_file in os.listdir(signal_dir):
        if not sph_file.endswith(".sph"):
            continue

        base_name = os.path.splitext(sph_file)[0]
        sph_path  = os.path.join(signal_dir, sph_file)
        trn_path  = os.path.join(trans_dir, base_name + ".trn")

        if not os.path.exists(trn_path):
            skipped_no_trn += 1
            continue

        text = clean_transcript(trn_path)
        if not text:
            skipped_empty += 1
            continue

        wav_out = os.path.join(OUTPUT_DIR, base_name + ".wav")
        txt_out = os.path.join(OUTPUT_DIR, base_name + ".txt")

        subprocess.call(
            f'ffmpeg -i "{sph_path}" -ar 16000 -ac 1 -sample_fmt s16 "{wav_out}" -loglevel error',
            shell=True
        )

        with open(txt_out, "w", encoding="utf-8") as f:
            f.write(text)

        processed += 1

print(f"\nDone. Processed: {processed} | Skipped (no trn): {skipped_no_trn} | Skipped (empty): {skipped_empty}")
