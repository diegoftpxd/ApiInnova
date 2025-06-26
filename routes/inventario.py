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

    dias_maximos_refrigerador = {
        'Manzana': 7,       
        'Palta': 4,        
        'Banana': 2,      
        'Porotos': 7,     
        'Mora': 3,              
        'Repollo': 14,    
        'Cactus': 10,            
        'Cajú': 5,             
        'Zanahoria': 21,      
        'Chirimoya': 3,      
        'Pepino': 7,            
        'Berenjena': 5,         
        'Grosella': 3,           
        'Pera': 5,                  
        'Pistacho': 180,             
        'Membrillo': 14,             
        'Tomate': 3,                 
        'Zapallito Italiano': 5,     
        'Cereza': 5,           
    }
    
    imagenes_disponibles = {
        "Manzana": 'https://media-public.canva.com/uqAe8/MAFDF5uqAe8/1/tl.png',
        "Kiwi": 'https://media-public.canva.com/-hCL8/MAFV79-hCL8/1/t.png',
        "Berenjena": 'https://www.pngplay.com/wp-content/uploads/2/Eggplant-Transparent-Images.png',
        "Banana": 'https://pngimg.com/d/banana_PNG844.png',
        "Tomate": 'https://www.pngplay.com/wp-content/uploads/2/Tomato-Transparent-Images.png',
        "Pepino": 'https://static.vecteezy.com/system/resources/thumbnails/029/720/727/small_2x/cucumber-transparent-background-png.png',
        "Zanahoria": 'https://static.vecteezy.com/system/resources/thumbnails/025/257/374/small/single-fresh-orange-carrot-isolated-with-clipping-path-and-shadow-in-file-format-close-up-of-healthy-vegetable-root-png.png' 
    }
    imagen_por_defecto = 'https://w7.pngwing.com/pngs/973/684/png-transparent-fresh-fruits-illustration-juice-auglis-euclidean-fruit-melon-fruit-natural-foods-food-strawberries-thumbnail.png'

    print([inv.vegetal for inv in inventarios])

    resultado = [
        {
            'id': inv.id,
            'name': inv.vegetal,
            'daysInUse': inv.dias,
            'expirationDays': dias_maximos_refrigerador[inv.vegetal],
            "photo": imagenes_disponibles.get(inv.vegetal, imagen_por_defecto),


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

