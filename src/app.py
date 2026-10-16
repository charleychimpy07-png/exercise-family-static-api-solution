import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Inicializamos la estructura de la familia Jackson
jackson_family = FamilyStructure("Jackson")

# 1. Obtener todos los miembros de la familia
@app.route('/members', methods=['GET'])
def handle_get_all_members():
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 2. Recuperar un solo miembro por ID
@app.route('/member/<int:member_id>', methods=['GET'])
@app.route('/members/<int:member_id>', methods=['GET'])
def handle_get_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if member:
            return jsonify(member), 200
        return jsonify({"error": "Miembro no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3. Añadir (POST) un nuevo miembro
@app.route('/member', methods=['POST'])
@app.route('/members', methods=['POST'])
def handle_add_member():
    try:
        request_body = request.get_json()
        if not request_body:
            return jsonify({"error": "Cuerpo de la solicitud inválido"}), 400

        new_member = jackson_family.add_member(request_body)
        return jsonify(new_member), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 4. Eliminar un miembro por ID
@app.route('/member/<int:member_id>', methods=['DELETE'])
@app.route('/members/<int:member_id>', methods=['DELETE'])
def handle_delete_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if not member:
            return jsonify({"error": "Miembro no encontrado"}), 404

        jackson_family.delete_member(member_id)
        return jsonify({"done": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)