from flask import Flask, request, redirect, render_template
import random
import string
tracker_list = ["ref", "&", "?", "?si", "?igsh", "&pp", "?itmmeta"]
app = Flask(__name__)

# basic in-memory storage (to replace this with a database later)
url_database = {}

@app.route('/')
def home():
    return render_template("index.html")

def generate_short_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))


@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form['url']

    # Generate unique code
    short_code = generate_short_code()

    # Save in "database"
    url_database[short_code] = long_url

    # Create the full short link
    short_link = f"http://localhost:5000/{short_code}"

    return f"Your short URL: <a href='{short_link}'>{short_link}</a>"


@app.route('/<short_code>')
def redirect_to_url(short_code):
    if short_code in url_database:
        original_url = url_database[short_code]
        return redirect(original_url)
    else:
        return "URL not found!"
# Send original URL
@app.route('/clean', methods=['POST'])
def remove_trackers():
    og_url=request.form['url']
    clean_url = og_url
    for word in tracker_list:
        if word in og_url:
            clean_url = og_url[:og_url.find(word)]
    return f"<a href='{clean_url}'>{clean_url}</a>"

if __name__ == "__main__":
    app.run(debug=True)

