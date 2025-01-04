from flask import Flask, render_template, request
from markdown import markdown
import yaml
import os

app = Flask(__name__)

# 添加 MIME types 設定
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['MIME_TYPES'] = {
    '.m4a': 'audio/aac',  # iPhone 語音備忘錄實際是 AAC 格式
    '.aac': 'audio/aac',
    '.mp3': 'audio/mpeg'
}

# 設定日誌記錄
app.logger.setLevel(0)

@app.after_request
def add_header(response):
    if 'audio' in response.mimetype:
        response.headers['Accept-Ranges'] = 'bytes'
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response

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
                    
                    # 分割主要內容和故事內容
                    if '## 延伸閱讀' in md:
                        main_content, story_content = md.split('## 延伸閱讀', 1)
                        metadata['story_content'] = markdown(story_content.strip(), extensions=['extra'])
                        metadata['story'] = True
                        md = main_content
                    
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
                
            return render_template('audio_guide.html', item=metadata)
    
    return "內容格式錯誤", 500

@app.route('/story/<category>/<item_name>')
def story(category, item_name):
    content_dir = os.path.join(os.path.dirname(__file__), 'content', category)
    file_path = os.path.join(content_dir, f"{item_name}.md")
    
    if not os.path.exists(file_path):
        return f"找不到指定的內容：{file_path}", 404
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if content.startswith('---'):
            _, fm, md = content.split('---', 2)
            metadata = yaml.safe_load(fm)
            
            # 分割主要內容和故事內容
            if '## 延伸閱讀' in md:
                _, story_content = md.split('## 延伸閱讀', 1)
                metadata['story_content'] = markdown(story_content.strip(), extensions=['extra'])
            else:
                return "找不到延伸閱讀內容", 404
            
            metadata['category'] = category
            return render_template('story.html', **metadata)
    
    return "內容格式錯誤", 500

if __name__ == '__main__':
    app.run(debug=True)
