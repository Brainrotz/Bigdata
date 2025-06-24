import os
import csv
import librosa

def get_bpm(file_path):
    try:
        y, sr = librosa.load(file_path, sr=None, mono=True)

        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)

        return round(float(tempo[0]), 2)
    except Exception as e:
        print(f"Error processing '{file_path}': {e}")
        return None

def process_folder(folder_path, output_csv="happy_results.csv"):
    results = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".mp3"):
            full_path = os.path.join(folder_path, filename)
            print(f"Processing: {filename}")
            bpm = get_bpm(full_path)
            if bpm:
                results.append([filename, bpm])
    
    # Write to CSV
    with open(output_csv, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "bpm"])
        writer.writerows(results)

    print(f"\n✅ BPM results saved to: {output_csv}")

if __name__ == "__main__":
    songs_folder = "happy"
    process_folder(songs_folder)
