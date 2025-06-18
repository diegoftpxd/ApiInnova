from flask import Blueprint, jsonify, request
from models import Inventario, Usuario, db

inventario_bp = Blueprint('inventario', __name__)



#Entrega el inventario si que no se ha consumido
@inventario_bp.route('/inventario', methods=['GET'])
def entregar_inventario():
    # En un query param se debe encviar id_usuario=NUMERO
    id_usuario = request.args.get('id_usuario', type=int)
    if not id_usuario:
        return jsonify({'error': 'Falta id_usuario como query parameter'}), 400

    inventarios = Inventario.obtener_por_usuario_no_consumidos(id_usuario)
    resultado = [
        {
            'id': inv.id,
            'vegetal': inv.vegetal,
            'peso': inv.peso,
            'dias': inv.dias,
            'consumido': inv.consumido
        } for inv in inventarios
    ]
    
    return jsonify(resultado), 200

#Entrega el inventario
@inventario_bp.route('/inventario', methods=['POST'])
def publicar_algo_en_inventario():

    # El body debe incluir ['id_usuario', 'vegetal', 'peso', 'dias', "consumido"]

    data = request.get_json()
    # Validación de campos requeridos
    campos_requeridos = ['id_usuario', 'vegetal', 'peso', 'dias', "consumido"]
    if not all(campo in data for campo in campos_requeridos):
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    try:
        nuevo = Inventario.crear(
            id_usuario=data['id_usuario'],
            vegetal=data['vegetal'],
            peso=data['peso'],
            dias=data['dias'],
            consumido=data['consumido']
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al crear inventario: {str(e)}'}), 500

    return jsonify({
        'id': nuevo.id,
        'vegetal': nuevo.vegetal,
        'peso': nuevo.peso,
        'dias': nuevo.dias,
        'consumido': nuevo.consumido
    }), 201


@inventario_bp.route('/inventario', methods=['DELETE'])
def borrar_elemento_inventario():

    # Recibe solo id en el body

    data = request.get_json()

    if not data or 'id' not in data:
        return jsonify({'error': 'Falta el campo id en el cuerpo de la solicitud'}), 400

    id_inventario = data['id']

    eliminado = Inventario.eliminar_por_id(id_inventario)
    if eliminado:
        return jsonify({'mensaje': f'Elemento con id {id_inventario} eliminado correctamente'}), 200
    else:
        return jsonify({'error': f'No se encontró un elemento con id {id_inventario}'}), 404


# Entrega la información completa de todo el inventario que se tiene
@inventario_bp.route('/inventario', methods=['GET'])
def entregar_inventario_completo():
    # En un query param se debe encviar id_usuario=NUMERO
    id_usuario = request.args.get('id_usuario', type=int)
    if not id_usuario:
        return jsonify({'error': 'Falta id_usuario como query parameter'}), 400

    inventarios = Inventario.obtener_por_usuario_todos(id_usuario)
    resultado = [
        {
            'id': inv.id,
            'vegetal': inv.vegetal,
            'peso': inv.peso,
            'dias': inv.dias,
            'consumido': inv.consumido
        } for inv in inventarios
    ]
    
    return jsonify(resultado), 200

