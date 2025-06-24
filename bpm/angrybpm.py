import yt_dlp
import librosa
import os
import csv
import uuid

def download_audio_from_youtube(url, output_dir="downloads"):
    os.makedirs(output_dir, exist_ok=True)
    unique_id = str(uuid.uuid4())
    output_template = os.path.join(output_dir, f"{unique_id}.%(ext)s")
    mp3_path = os.path.join(output_dir, f"{unique_id}.mp3")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return mp3_path

def get_bpm(file_path):
    try:
        y, sr = librosa.load(file_path, sr=None, mono=True)
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)
        return round(float(tempo[0]), 2)
    except Exception as e:
        print(f"Error processing '{file_path}': {e}")
        return None

def analyze_youtube_links(url_list, output_csv="angry_bpm_results.csv", cleanup=True):
    results = []

    for url in url_list:
        print(f"🔍 Downloading and analyzing: {url}")
        try:
            mp3_path = download_audio_from_youtube(url)
            bpm = get_bpm(mp3_path)
            if bpm:
                results.append([url, bpm])
            if cleanup and os.path.exists(mp3_path):
                os.remove(mp3_path)
        except Exception as e:
            print(f"❌ Failed for {url}: {e}")

    # Save to CSV
    with open(output_csv, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["YouTube URL", "BPM"])
        writer.writerows(results)

    print(f"\n✅ BPM analysis complete. Results saved to: {output_csv}")

if __name__ == "__main__":
    youtube_links = [
        "https://www.youtube.com/watch?v=xAUaEfzt_VU&ab_channel=MetalMusic",
        "https://www.youtube.com/watch?v=v-RhGvM8Nng&ab_channel=Gustinho",
        "https://www.youtube.com/watch?v=FtOnSQvz8yc&ab_channel=DrecoTheDragon88",
        "https://www.youtube.com/watch?v=sKtl7-_6AjE&ab_channel=LinkinPark-Topic",
        "https://www.youtube.com/watch?v=qqK1FrO3BdM&ab_channel=Slipknot",
        "https://www.youtube.com/watch?v=rmFWsIIuMbA&ab_channel=MattT02",
        "https://www.youtube.com/watch?v=sMvTB9UHPBY&ab_channel=Beabadoobee-Topic",
        "https://www.youtube.com/watch?v=6ELX91ChFvs&ab_channel=zakoneill",
        "https://www.youtube.com/watch?v=53ulHedroTk&ab_channel=MachineGirl-Topic",
        "https://www.youtube.com/watch?v=OVFR9csRyoM&ab_channel=MachineGirl-Topic",
        "https://www.youtube.com/watch?v=U85MJA1vGSI&ab_channel=MachineGirl-Topic",
        "https://www.youtube.com/watch?v=ZylLAj2iId4&ab_channel=50Cent-Topic",
        "https://www.youtube.com/watch?v=0YdLT0rL6L4&ab_channel=BaileyMusicUnedited2",
        "youtube.com/watch?v=qZuxPKUVGiw",
        "https://www.youtube.com/watch?v=g0PoaU4PkQk&ab_channel=slayyystan",
        "https://www.youtube.com/watch?v=Nd1j7ETVtd8&ab_channel=DizzeeRascal-Topic",
        "https://www.youtube.com/watch?v=NudG26B_m_c&ab_channel=POOMPLEX2",
        "https://www.youtube.com/watch?v=Il_51tSLadg&ab_channel=MachineGirl-Topic",
        "https://www.youtube.com/watch?v=JRiSdAe8sGY&ab_channel=EpitaphRecords",
        "https://www.youtube.com/watch?v=d7PPjEB2QZQ&ab_channel=Beyonc%C3%A9VEVO",
        "https://www.youtube.com/watch?v=T9iHXEXKX4Q&ab_channel=scarlxrd",
        "https://www.youtube.com/watch?v=CMA-Y7A_7tA&ab_channel=KAMAARA",
        "https://www.youtube.com/watch?v=UwToIoVNLVk&ab_channel=Istasha-Topic",
        "https://www.youtube.com/watch?v=Gei_SKgrMpI&ab_channel=KillDyll",
        "https://www.youtube.com/watch?v=CFfzw8Xe6Sw&ab_channel=Kayzo-Topic",
        "https://www.youtube.com/watch?v=0f0rfJbLNDc&ab_channel=Kayzo-Topic",
        "https://www.youtube.com/watch?v=L6s1nRzCUSI&ab_channel=Scarlxrd-Topic",
        "https://www.youtube.com/watch?v=3Qnco949TrM&ab_channel=scarlxrd",
        "https://www.youtube.com/watch?v=FdBqOCS8LmM&ab_channel=Slipknot",
        "https://www.youtube.com/watch?v=26vk64g-Se0&ab_channel=MachineGirl-Topic",
        "https://www.youtube.com/watch?v=PhHDd-AglXk&ab_channel=FionaApple-Topic",
        "https://www.youtube.com/watch?v=VR24Pfw7Ykw&ab_channel=DenzelCurry-Topic",
        "https://www.youtube.com/watch?v=r-eKJIJXaqE&ab_channel=Metalocalypse%3ADethklok%7CMusic",
        "youtube.com/watch?v=tPeCHvAJCEQ",
        "https://www.youtube.com/watch?v=-LdYXYNtPJI&ab_channel=ScarecrowYard",
        "https://www.youtube.com/watch?v=pfCI8NMq5xE&ab_channel=riotwav",
        "https://www.youtube.com/watch?v=OPiDMM6YwFA&ab_channel=ChaseAndStatusVEVO",
        "https://www.youtube.com/watch?v=kmg8EAD-Kjw&ab_channel=BabyLasagna",
        "https://www.youtube.com/watch?v=o1dZkg6-eOw&ab_channel=DarkCitySounds",
        "https://www.youtube.com/watch?v=U-b5gDWVnps&ab_channel=K%C3%A4%C3%A4rij%C3%A4",
        "https://www.youtube.com/watch?v=wJGcwEv7838&ab_channel=XXXTENTACION",
        "https://www.youtube.com/watch?v=7SM5laxokpg&ab_channel=MyChemicalRomance-Topic",
        "https://www.youtube.com/watch?v=cj3U0z64_m4&ab_channel=TheHalluciNation",
        "https://www.youtube.com/watch?v=QwyZ1gOhU_o&ab_channel=SystemOfADown-Topic",
        "https://www.youtube.com/watch?v=v6HBZC9pZHQ&ab_channel=BabyKeemVEVO",
        "https://www.youtube.com/watch?v=kQrLZp-BKVw&ab_channel=JuanGM"
        # Add more links here
    ]

    analyze_youtube_links(youtube_links)
