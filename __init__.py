from cryptography.fernet import Fernet, InvalidToken
from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

key = Fernet.generate_key()
f = Fernet(key)

@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    token = f.encrypt(valeur_bytes)  # Encrypt la valeur
    return f"Valeur encryptée : {token.decode()}"  # Retourne le token en str
@app.route('/decrypt/<string:valeur>')
def decryptage(valeur):
    try:
        valeur_bytes = valeur.encode()
        decrypted = f.decrypt(valeur_bytes)
        return f"Valeur décryptée : {decrypted.decode()}"
    except:
        return "Erreur : valeur non déchiffrable"
@app.route('/generate-key/', methods=['GET'])
def generate_key():
    key = Fernet.generate_key().decode()
    return jsonify({'key': key})
@app.route('/encrypt/', methods=['POST'])
def encrypt_post():
    try:
        data = request.get_json()
        key = data['key'].encode()
        message = data['message'].encode()

        f = Fernet(key)
        encrypted_token = f.encrypt(message).decode()
        return jsonify({'encrypted_token': encrypted_token})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/decrypt/', methods=['POST'])
def decrypt_post():
    try:
        data = request.get_json()
        key = data['key'].encode()
        token = data['token'].encode()

        f = Fernet(key)
        decrypted_message = f.decrypt(token).decode()
        return jsonify({'decrypted_message': decrypted_message})
    except InvalidToken:
        return jsonify({'error': 'Token invalide ou clé incorrecte'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400
      
                                                                                                                                                     
if __name__ == "__main__":
  app.run(debug=True)
#kakou kakou
