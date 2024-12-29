from flask import Flask, render_template, request

app = Flask(__name__)

@app.context_processor
def utility_processor():
    def is_active(endpoint):
        return 'active' if request.endpoint == endpoint else ''
    return dict(is_active=is_active)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/food')
def food():
    return render_template('food.html')

@app.route('/culture')
def culture():
    return render_template('culture.html')

@app.route('/shopping')
def shopping():
    return render_template('shopping.html')

if __name__ == '__main__':
    app.run(debug=True)
