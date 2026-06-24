import os
import re
import string
import subprocess
import soundfile as sf
from tqdm import tqdm

DATA_DIR   = "input"
OUTPUT_DIR = "output"

MIN_DUR = 10.0
MAX_DUR = 20.0

SPLITS = ["train", "test"]

for split in SPLITS:
    input_dir  = os.path.join(DATA_DIR, split)
    output_dir = os.path.join(OUTPUT_DIR, split)
    os.makedirs(output_dir, exist_ok=True)

    skipped_duration = 0
    skipped_empty    = 0
    processed        = 0

    print(f"\nProcessing {split}...")

    for root, dirs, files in tqdm(os.walk(input_dir)):
        for file in files:
            if not file.endswith(".flac"):
                continue

            flac_path = os.path.join(root, file)
            trn_path  = flac_path.replace(".flac", ".trn")

            if not os.path.exists(trn_path):
                continue

            info = sf.info(flac_path)
            if not (MIN_DUR <= info.duration <= MAX_DUR):
                skipped_duration += 1
                continue

            with open(trn_path, "r", encoding="utf-8") as f:
                text = f.readline().strip().lower()

            if not text:
                skipped_empty += 1
                continue

            base_name = os.path.splitext(file)[0]
            wav_out   = os.path.join(output_dir, base_name + ".wav")
            txt_out   = os.path.join(output_dir, base_name + ".txt")

            subprocess.call(
                f'ffmpeg -i "{flac_path}" -ar 16000 -ac 1 -sample_fmt s16 "{wav_out}" -loglevel error',
                shell=True
            )

            with open(txt_out, "w", encoding="utf-8") as f:
                f.write(text)

            processed += 1

    print(f"{split}: processed {processed} | skipped by duration {skipped_duration} | skipped empty {skipped_empty}")
