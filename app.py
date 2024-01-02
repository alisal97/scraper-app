from flask import Flask, request, jsonify
from MODULES.scraper import finder, get_content  
import logging
import config 

app = Flask (__name__)

logging.basicConfig(filename='flask_app.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/scraper-app', methods=['POST'])
def scrape():
    data = request.json
    if not data or 'urls' not in data:
        return jsonify({'error': 'No URLs provided'}), 400

    results = []
    for url in data['urls']:
        links = finder(url)

        if links and not "Contact page not found." in links:
            for link in links:
                content = get_content(link)
                if content:
                    results.append({
                        'url': link,
                        'content': content
                    })
        else:
            return jsonify({'error': f'Relevant pages not found for URL: {url}'}), 404

    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=True, port=config.port)
