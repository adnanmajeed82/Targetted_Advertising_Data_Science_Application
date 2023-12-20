import random
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_user_data():
    # Gather user interests via a form (replace with your preferred method)
    return request.args.get('interests') or ''

def fetch_targeted_ads(user_data):
    ads = []
    if user_data:
        keywords = user_data.split(',')
        for keyword in keywords:
            # Perform a Google search for the keyword
            response = requests.get(f"https://www.google.com/search?q={keyword}")
            response.raise_for_status()

            # Parse the HTML to extract potential ad links and images
            soup = BeautifulSoup(response.text, 'html.parser')
            potential_ads = soup.find_all('a', href=True)

            # Randomly select a few ads and construct ad objects
            for ad_link in random.sample(potential_ads, 3):
                ad_title = ad_link.text.strip()
                ad_image_url = ad_link.find('img')['src'] if ad_link.find('img') else None
                ads.append({'title': ad_title, 'link': ad_link['href'], 'image_url': ad_image_url})

    return ads

@app.route('/')
def index():
    interests = get_user_data()
    ads = fetch_targeted_ads(interests)
    return render_template('index.html', ads=ads)

if __name__ == '__main__':
    app.run(debug=True)