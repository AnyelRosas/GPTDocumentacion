from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/buscar-documentacion', methods=['POST'])
def buscar_documentacion():
    data = request.json
    enlaces = data.get('enlaces')
    if not enlaces:
        return jsonify({'message': 'No se proporcionaron enlaces'}), 400

    all_text = ""
    for enlace in enlaces:
        response = requests.get(enlace)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            text_content = ''
            for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'li']):
                text_content += tag.get_text() + '\n'
            all_text += f'Documentación de {enlace}:\n\n{text_content}\n\n'

    filename = 'documentacion.txt'
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(all_text)

    return jsonify({'message': 'Documento generado con éxito', 'archivo': filename}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
