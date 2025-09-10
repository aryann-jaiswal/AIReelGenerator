import os, time
from text_to_audio import text_to_speech_file
import subprocess

def text_to_audio(folder):
    print("Text To Audio: ", folder)
    with open(f"user_uploads/{folder}/desc.txt") as f:
        text = f.read()
    print(text, folder)
    text_to_speech_file(text, folder)

def create_reel(folder):
    output_dir = "static/reels"
    os.makedirs(output_dir, exist_ok=True)  # creates the folder if it doesn't exist

    output_file = os.path.join(output_dir, f"{folder}.mp4")
    command = f'ffmpeg -f concat -safe 0 -i user_uploads/{folder}/input.txt -i user_uploads/{folder}/audio.mp3 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p static/reels/{folder}.mp4'

    subprocess.run(command, shell=True, check=True)
    print("Create Reel: ", folder)


if __name__ == "__main__":
    if __name__ == "__main__":
        while True:
            with open("done.txt", "r") as f:
                done_folders = [line.strip() for line in f if line.strip()]

            folders = [f for f in os.listdir("user_uploads") if os.path.isdir(os.path.join("user_uploads", f))]

            for folder in folders:
                if folder not in done_folders:
                    print("Processing folder:", folder)
                    try:
                        text_to_audio(folder)
                        create_reel(folder)
                    except Exception as e:
                        print("Error processing folder", folder, ":", e)
                        continue

                    with open("done.txt", "a") as f:
                        f.write(folder + "\n")

            time.sleep(4)