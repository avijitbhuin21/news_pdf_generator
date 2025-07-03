from flask import Flask, request, jsonify
from handler_functions import *
import os
import json


app = Flask(__name__)



@app.route('/')
def hello():
    return open('html_templates/homepage.html').read()




@app.route('/get_news')
def get_news():
    return get_trending_news()

@app.route('/display_pdf', methods=['POST'])
def display_pdf():
    data = request.json
    if not data or 'content' not in data:
        return jsonify({'error': 'No URL provided'}), 400
    dd = data['content']
    print(dd)
    pdf_content = get_page_html(dd)
    print(pdf_content)
    if pdf_content is None:
        return jsonify({'error': 'PDF content not found'}), 404
    return jsonify({'content': pdf_content}), 200

@app.route('/get_pdfs')
def get_pdfs():
    database_path = 'database'
    if not os.path.exists(database_path):
        return jsonify({'pdfs': []}), 200
    
    pdf_files = [f.replace('.json', '') for f in os.listdir(database_path) if f.endswith('.json')]
    return jsonify({'pdfs': pdf_files}), 200

@app.route('/create_pdf', methods=['POST'])
def create_pdf():
    data = request.json
    if not data or 'url' not in data:
        return jsonify({'error': 'No Name provided'}), 400
    name = data['url']
    
    # Check if file already exists
    file_path = f'database/{name}.json'
    if os.path.exists(file_path):
        return jsonify({'error': 'PDF with this name already exists'}), 409
    
    content = data.get('content', '')
    with open(file_path, 'w') as f:
        f.write(content)

    return jsonify({'message': 'PDF created successfully', 'name': name}), 200

@app.route('/delete_pdf/<name>', methods=['DELETE'])
def delete_pdf(name):
    file_path = f'database/{name}.json'
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'message': 'PDF deleted successfully', 'name': name}), 200
    else:
        return jsonify({'error': 'PDF not found'}), 404

@app.route('/update_pdf/<name>', methods=['PUT'])
def update_pdf(name):
    data = request.json
    if not data or 'content' not in data:
        return jsonify({'error': 'No content provided'}), 400
    
    file_path = f'database/{name}.json'
    if not os.path.exists(file_path):
        return jsonify({'error': 'PDF not found'}), 404
    
    content = data['content']
    ll = open(file_path, 'r').read()
    existing_content = json.loads(ll) if ll != '' else []
    content = existing_content + content
    with open(file_path, 'w') as f:
        json.dump(content, f)
    
    return jsonify({'message': 'PDF updated successfully', 'name': name}), 200

@app.route('/get_pdf_content/<name>')
def get_pdf_content(name):
    file_path = f'database/{name}.json'
    if not os.path.exists(file_path):
        return jsonify({'error': 'PDF not found'}), 404
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    return jsonify({'name': name, 'content': content}), 200

if __name__ == '__main__':
    # install the necessary packages
    install_wkhtmltopdf()
    # Ensure the database directory exists
    if not os.path.exists('database'):
        os.makedirs('database')
    app.run(debug=True)