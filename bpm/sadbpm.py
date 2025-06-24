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

def analyze_youtube_links(url_list, output_csv="sad_bpm_results.csv", cleanup=True):
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
        "https://www.youtube.com/watch?v=t_0C9rQBCSE&ab_channel=Amir",
        "https://www.youtube.com/watch?v=rtNZK3PUme8&ab_channel=SautiSol",
        "https://www.youtube.com/watch?v=Mcv1vdkLmhk&ab_channel=RIFFTASTIC",
        "https://www.youtube.com/watch?v=5XtjPMdPN1o&ab_channel=CurrentJoys-Topic",
        "https://www.youtube.com/watch?v=Bfurc6KcMwk&ab_channel=Mitski",
        "https://www.youtube.com/watch?v=XfMBdq5iFnw&ab_channel=Mitski",
        "https://www.youtube.com/watch?v=-0XFfIf3MAw&ab_channel=LyricParadise",
        "https://www.youtube.com/watch?v=BjGB9hc5huk&ab_channel=DeadOceans",
        "https://www.youtube.com/watch?v=tJnzKWKhRUM&ab_channel=OklouVEVO",
        "https://www.youtube.com/watch?v=AuHHs4JvgLs&ab_channel=CarolinePolachek-Topic",
        "https://www.youtube.com/watch?v=-Hd4XyhfRQg&ab_channel=ObsidianMusic",
        "https://www.youtube.com/watch?v=3jHYzJUoGB0&ab_channel=AmyWinehouse-Topic",
        "https://www.youtube.com/watch?v=T6HDrFxDVX8&ab_channel=CarolinePolachekVEVO",
        "https://www.youtube.com/watch?v=4HLumkaPcCI&ab_channel=KeshiVEVO",
        "https://www.youtube.com/watch?v=AJ75-7IIjRs&ab_channel=keshi-Topic",
        "https://www.youtube.com/watch?v=08GuBjFgWUk&ab_channel=SonnyZero-Topic",
        "https://www.youtube.com/watch?v=w9_l7tv-Mag&ab_channel=ShanShanImperial",
        "https://www.youtube.com/watch?v=3NCuqTrE3lU&ab_channel=felix",
        "https://www.youtube.com/watch?v=XKQjQYuqHkY&ab_channel=Faceless1-7",
        "https://www.youtube.com/watch?v=Hp6jtxkoxzM&ab_channel=Faceless1-7",
        "https://www.youtube.com/watch?v=eMKCeLgA2IY&ab_channel=KillDyll",
        "https://www.youtube.com/watch?v=9sQ18XhRNqM&ab_channel=.33DELIRIUM-Topic",
        "https://www.youtube.com/watch?v=C3pxv01Ysq4&ab_channel=Istasha-Topic",
        "https://www.youtube.com/watch?v=x9s0XIdW_m8&ab_channel=Scarlxrd-Topic",
        "https://www.youtube.com/watch?v=3yppxrBiBts&ab_channel=KingKrule-Topic",
        "https://www.youtube.com/watch?v=_eACTXi1DTc&ab_channel=Lyricz",
        "https://www.youtube.com/watch?v=KuRoG6s2kO4&ab_channel=d.ear-Topic",
        "https://www.youtube.com/watch?v=_QvNCKjPyOU&ab_channel=B%C2%A1ttersweettBabyy%F0%9F%96%A4",
        "https://www.youtube.com/watch?v=Bfurc6KcMwk&ab_channel=Mitski",
        "https://www.youtube.com/watch?v=XfMBdq5iFnw&ab_channel=Mitski",
        "https://www.youtube.com/watch?v=vnw8zURAxkU&ab_channel=%E3%83%92%E3%83%88%E3%83%AA%E3%82%A8%2Fwowaka",
        "https://www.youtube.com/watch?v=OwGG5fX7bxY&ab_channel=MecanoVEVO",
        "https://www.youtube.com/watch?v=XoEm0jcqVHg&ab_channel=FreeLines",
        "https://www.youtube.com/watch?v=11Qj2Tpkh0U&ab_channel=DeadOceans",
        "https://www.youtube.com/watch?v=laXY5e5JaV0&ab_channel=TheSmiths",
        "https://www.youtube.com/watch?v=Ddak8jVdMR8&ab_channel=FionaApple-Topic",
        "https://www.youtube.com/watch?v=rqHKwjk6_Gk",
        "youtube.com/watch?v=w1aeuuklqXM",
        "https://www.youtube.com/watch?v=7JGDWKJfgxQ&ab_channel=XXXTENTACION",
        "https://www.youtube.com/watch?v=FAucVNRx_mU&ab_channel=XXXTENTACION",
        "https://www.youtube.com/watch?v=Z0uwqYId4SM&ab_channel=Stract",
        "https://www.youtube.com/watch?v=Ifwf8RrU-94&ab_channel=HIMVEVO",
        "https://www.youtube.com/watch?v=7ly7Mhle-4M&ab_channel=sagun",
        "https://www.youtube.com/watch?v=7SM5laxokpg&ab_channel=MyChemicalRomance-Topic",
        "https://www.youtube.com/watch?v=lIqBXPtolcw&ab_channel=CdyJaquesMCR",
        "https://www.youtube.com/watch?v=jUkoL9RE72o",
        "youtube.com/watch?v=pGhwBFYtn1s",
        "https://www.youtube.com/watch?v=hXQwIoE_5ko&ab_channel=AquaLyrics"
        # Add more links here
    ]

    analyze_youtube_links(youtube_links)
