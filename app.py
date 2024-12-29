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

if __name__ == '__main__':
    app.run(debug=True)
