
import mysql.connector
import time
from flask import Flask, request, jsonify
from config import MYSQL_CONFIG

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(**MYSQL_CONFIG)

@app.route('/dispersion', methods=['POST'])
def insert_dispersion():
    try:
        data = request.get_json()

        url = data.get('url')
        funcion = data.get('funcion')
        created_at	 = int(time.time())  # Fecha actual en segundos UNIX

        if not url or not funcion:
            return jsonify({'error': 'Faltan datos: url o funcion'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        query = "INSERT INTO tn_dispersion (url, funcion,created_at ) VALUES (%s, %s, %s)"
        cursor.execute(query, (url, funcion, created_at	))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({'message': 'Registro insertado correctamente'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({'status': 'API OK'}), 200

@app.route("/health")
def health():
    return jsonify({
        "status": "UP"
    }), 200


@app.route("/version")
def version():
    return jsonify({
        "service": "ms_ia_dispersion",
        "version": "1.0.0"
    }), 200


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)

