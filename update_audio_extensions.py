import os
import yaml
import glob

def update_audio_extensions():
    # 獲取所有 md 檔案
    content_files = glob.glob('content/**/*.md', recursive=True)
    
    for file_path in content_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if content.startswith('---'):
            try:
                # 分割 YAML front matter
                _, fm, md = content.split('---', 2)
                metadata = yaml.safe_load(fm)
                
                # 檢查是否有音訊檔案設定
                if 'audio' in metadata and metadata['audio'].endswith('.m4a'):
                    # 更新音訊檔案副檔名
                    metadata['audio'] = metadata['audio'].replace('.m4a', '.mp3')
                    
                    # 重建 front matter
                    new_fm = yaml.dump(metadata, allow_unicode=True)
                    new_content = f"---\n{new_fm}---{md}"
                    
                    # 寫回檔案
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated {file_path}")
                        
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")

if __name__ == "__main__":
    update_audio_extensions()
