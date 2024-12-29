from flask import Flask, render_template, request
from markdown import markdown
import yaml
import os

app = Flask(__name__)

def load_content(directory):
    items = []
    content_dir = os.path.join(os.path.dirname(__file__), 'content', directory)
    
    if not os.path.exists(content_dir):
        return items
        
    for filename in os.listdir(content_dir):
        if filename.endswith('.md'):
            with open(os.path.join(content_dir, filename), 'r', encoding='utf-8') as f:
                content = f.read()
                # 分割 YAML front matter 和 markdown 內容
                if content.startswith('---'):
                    _, fm, md = content.split('---', 2)
                    metadata = yaml.safe_load(fm)
                    html_content = markdown(md.strip(), extensions=['extra'])
                    metadata['content'] = html_content
                    # 使用文件名（不含副檔名）作為 id
                    if 'id' not in metadata:
                        metadata['id'] = os.path.splitext(filename)[0]
                    items.append(metadata)
    
    return items

@app.context_processor
def utility_processor():
    return dict(active_page=lambda p: 'active' if p == request.endpoint else '')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/food')
def food():
    items = load_content('food')
    return render_template('food.html', items=items)

@app.route('/culture')
def culture():
    items = load_content('culture')
    return render_template('culture.html', items=items)

@app.route('/shopping')
def shopping():
    items = load_content('shopping')
    return render_template('shopping.html', items=items)

@app.route('/audio-guide/<category>/<item_name>')
def audio_guide(category, item_name):
    content_dir = os.path.join(os.path.dirname(__file__), 'content', category)
    file_path = os.path.join(content_dir, f"{item_name}.md")
    
    if not os.path.exists(file_path):
        return f"找不到指定的內容：{file_path}", 404
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if content.startswith('---'):
            _, fm, md = content.split('---', 2)
            metadata = yaml.safe_load(fm)
            html_content = markdown(md.strip(), extensions=['extra'])
            metadata['content'] = html_content
            if 'id' not in metadata:
                metadata['id'] = item_name
                
            # 檢查音頻文件格式
            audio_filename = metadata.get('audio', '')
            if audio_filename:
                # 優先使用 m4a 格式
                m4a_filename = audio_filename.rsplit('.', 1)[0] + '.m4a'
                mp3_filename = audio_filename
                
                # 檢查文件是否存在
                m4a_path = os.path.join(app.static_folder, 'audio', m4a_filename)
                mp3_path = os.path.join(app.static_folder, 'audio', mp3_filename)
                
                if os.path.exists(m4a_path):
                    metadata['audio'] = m4a_filename
                elif os.path.exists(mp3_path):
                    metadata['audio'] = mp3_filename
                else:
                    return f"找不到音頻文件：{m4a_filename} 或 {mp3_filename}", 404
                    
            return render_template('audio_guide.html', item=metadata)
    
    return "內容格式錯誤", 500

if __name__ == '__main__':
    app.run(debug=True)
