from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
url = "https://isaretce.com/"

def get_gif_link(query):
    res = requests.get(url, params={'s': query})
    soup = BeautifulSoup(res.content, "html.parser")
    if len(soup.find_all('body', class_="search-no-results")) > 0:
        return None
    return soup.find('img', class_='alignnone').get('src')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        q = query.lower().split()
        results = {}
        for k in q:
            results[k] = get_gif_link(k)
        return render_template('index.html', results=results)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
