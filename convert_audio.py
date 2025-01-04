import os
from pydub import AudioSegment
import glob

def convert_m4a_to_mp3():
    # 獲取所有 m4a 檔案
    audio_dir = os.path.join(os.path.dirname(__file__), 'static', 'audio')
    m4a_files = glob.glob(os.path.join(audio_dir, '*.m4a'))
    
    for m4a_file in m4a_files:
        # 建立對應的 mp3 檔案名
        mp3_file = m4a_file.replace('.m4a', '.mp3')
        
        # 如果 mp3 檔案已存在，跳過
        if os.path.exists(mp3_file):
            print(f"Skipping {os.path.basename(m4a_file)} (already converted)")
            continue
            
        try:
            # 載入 m4a 檔案
            audio = AudioSegment.from_file(m4a_file, format="m4a")
            
            # 轉換並儲存為 mp3
            audio.export(mp3_file, format="mp3", bitrate="192k")
            print(f"Converted {os.path.basename(m4a_file)} to MP3")
        except Exception as e:
            print(f"Error converting {os.path.basename(m4a_file)}: {str(e)}")

if __name__ == "__main__":
    convert_m4a_to_mp3()
