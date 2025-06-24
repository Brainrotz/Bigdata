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

def analyze_youtube_links(url_list, output_csv="happybpm_csv.csv", cleanup=True):
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
        "https://www.youtube.com/watch?v=jffGXR7vNdk&ab_channel=PIPASON2123",
        "https://www.youtube.com/watch?v=z95GDkzjezY&ab_channel=SweetFemaleAttitude-Topic",
        "https://www.youtube.com/watch?v=gzmdrobXH34&ab_channel=QadiWafi",
        "https://www.youtube.com/watch?v=ihZBS3D2u3I&ab_channel=JaneRemover",
        "https://www.youtube.com/watch?v=rTdeERCeyNk&ab_channel=NinaNesbitt",
        "https://www.youtube.com/watch?v=Iapw_hbyBjE&ab_channel=SonySoundtracksVEVO",
        "https://www.youtube.com/watch?v=3YSUvYDJ6R4&ab_channel=WayneWonder-Topic",
        "https://www.youtube.com/watch?v=cB1TERquEYI&ab_channel=SoulfulG",
        "https://www.youtube.com/watch?v=SIBRmK74Tzk&ab_channel=Earth%2CWind%26Fire-Topic",
        "https://www.youtube.com/watch?v=sbOk0unnlbw&ab_channel=Lyrics90%27s",
        "https://www.youtube.com/watch?v=fI569nw0YUQ&ab_channel=CherylLynnVEVO",
        "https://www.youtube.com/watch?v=8D4hcrkI2xU&ab_channel=EarthWindandFireVEVO",
        "https://www.youtube.com/watch?v=1ZZQuj6htF4&ab_channel=michaeljacksonVEVO",
        "https://www.youtube.com/watch?v=79sU9UXD5eA&ab_channel=JaneRemover",
        "https://www.youtube.com/watch?v=TEKtdaFclao&ab_channel=TheMaryWallopers-Topic",
        "https://www.youtube.com/watch?v=oT9gDtObhzY&ab_channel=cr1tter-Topic",
        "https://www.youtube.com/watch?v=vGPtQicI3IE&ab_channel=DerikFeinVEVO",
        "https://www.youtube.com/watch?v=k7NZYuFIGzg&ab_channel=Cr1tter",
        "https://www.youtube.com/watch?v=smVU37xAhY8&ab_channel=draingang",
        "https://www.youtube.com/watch?v=H5D18nAWDKw&ab_channel=cr1tter-Topic",
        "https://www.youtube.com/watch?v=vpV3xThmbVo&ab_channel=IDERVEVO",
        "https://www.youtube.com/watch?v=KWxM_zLJGsU&ab_channel=COINVEVO",
        "https://www.youtube.com/watch?v=TMcr78zNXJ4&ab_channel=velvetign",
        "https://www.youtube.com/watch?v=PoWoWiqI3aM&list=PLklogUjfGREWkLIBAt4qsdTJd9ACjWud5&index=10&ab_channel=JAMPHARLD",
        "https://www.youtube.com/watch?v=7yD6uegaP5w&ab_channel=KSECTORLYRICS",
        "https://www.youtube.com/watch?v=VJGaVkDpWr4&ab_channel=lexycat-Topic",
        "https://www.youtube.com/watch?v=jF43xtZucsw&ab_channel=Billlie",
        "https://www.youtube.com/watch?v=sEaH-WtdkxQ&ab_channel=GFRIEND-Topic",
        "https://www.youtube.com/watch?v=OL2bg-byJn8&list=PLfJndz0utgONTZbXDDmN8oXm4ks4v8IOL&index=3&ab_channel=JunkFujiyama-Topic",
        "https://www.youtube.com/watch?v=adVx8OMXdLM",
        "https://www.youtube.com/watch?v=RWYA9BvxMso",
        "https://www.youtube.com/watch?v=JV-IOJX7t7w",
        "https://www.youtube.com/watch?v=CdqxbdUvDQo&ab_channel=Frederic-Topic",
        "https://www.youtube.com/watch?v=L1ByttunrDs&ab_channel=cosMo%40%E6%9A%B4%E8%B5%B0P",
        "https://www.youtube.com/watch?v=pJ-MywdW98o&ab_channel=Tia-Topic",
        "https://www.youtube.com/watch?v=4sq2lPNxi7M&ab_channel=ReolOfficial",
        "https://www.youtube.com/watch?v=p-o_bMkzOW0&ab_channel=ReolOfficial",
        "https://www.youtube.com/watch?v=uQ9_MwZIaoc&ab_channel=BeeGeesVEVO",
        "https://www.youtube.com/watch?v=hyV4qGAPKac&ab_channel=googoo888",
        "https://www.youtube.com/watch?v=LGeD9cN7ndA&ab_channel=krystalized",
        "https://www.youtube.com/watch?v=X5s2e9cX_TI&ab_channel=RedVelvet-Topic",
        "youtube.com/watch?v=FLuhVsDFOh8",
        "https://www.youtube.com/watch?v=-4crkwvrL4k&ab_channel=Jenirus",
        "https://www.youtube.com/watch?v=OOXmduldV3Q&ab_channel=redxheart",
        "https://www.youtube.com/watch?v=RZMOvrWj_cE&ab_channel=SHINee-Topic",
        "https://www.youtube.com/watch?v=-QHLKZJQrKg&ab_channel=SHINee-Topic",
        "https://www.youtube.com/watch?v=1Yr9IsQo3_c&ab_channel=TheeSacredSouls",
        "https://www.youtube.com/watch?v=5JciEg-kyKo&ab_channel=EpicVibes",
        "https://www.youtube.com/watch?v=W-PGNyhmSKA&ab_channel=OliviaRodrigoVEVO",
        "https://www.youtube.com/watch?v=1O-tCjveBho&ab_channel=Pinkpantheress",
        "https://www.youtube.com/watch?v=bJx1hntfzOI&ab_channel=ATARASHIIGAKKO%21-%E6%96%B0%E3%81%97%E3%81%84%E5%AD%A6%E6%A0%A1%E3%81%AE%E3%83%AA%E3%83%BC%E3%83%80%E3%83%BC%E3%82%BA",
        "https://www.youtube.com/watch?v=kmG9sWo5Tw0&ab_channel=WhiteBoxNinjah",
        "https://www.youtube.com/watch?v=rOnxmiaUQK0&ab_channel=slickprd",
        "https://www.youtube.com/watch?v=zHoZ2gPTUHM&ab_channel=VibeMusic",
        "https://www.youtube.com/watch?v=bUwHblpMX1M&ab_channel=yankat",
        "https://www.youtube.com/watch?v=gInOau6EFdI&ab_channel=LatinHype",
        "https://www.youtube.com/watch?v=UsJ7g988dSo&ab_channel=Yaku",
        "https://www.youtube.com/watch?v=qparhhC1YB0&ab_channel=TrendingTracks",
        "https://www.youtube.com/watch?v=fhrK0i-2Nes&ab_channel=MajesticVibes",
        "https://www.youtube.com/watch?v=k6Vu7SRMlFk&ab_channel=mrlgjj"
    ]
    analyze_youtube_links(youtube_links)