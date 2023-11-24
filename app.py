from flask import Flask, request, jsonify
from MODULES.scraper import finder, get_content  
import logging
import config 

app = Flask(__name__)

logging.basicConfig(filename='flask_app.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.json
    if not data or 'url' not in data:
        return jsonify({'error': 'No URL provided'}), 400

    url = data['url']
    links = finder(url)

    if links and not "Contact page not found." in links:
        results = []
        for link in links:
            content = get_content(link)
            if content:
                results.append({
                    'url': link,
                    'content': content
                })
        return jsonify(results), 200
    else:
        return jsonify({'error': 'Relevant pages not found.'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=config.port)
