from flask import Blueprint, jsonify, request
from models import Inventario, Usuario, db
from elección_vegetal import analizar_imagen
from PIL import Image
import os
import uuid

dispositivo_bp = Blueprint('dispositivo', __name__)
#from your_module import FUNCION_IA  # Asegúrate de importar correctamente

def FUNCION_IA(ruta_imagen):
    return "lechuga"



@dispositivo_bp.route('/dispositivo', methods=['POST'])
def recibir_nuevos_datos_desde_dispositivo():
    print(request.files)
    print(request.form)

    if 'imagen' not in request.files or 'peso' not in request.form or 'id_usuario' not in request.form:
        return jsonify({'error': 'Faltan campos requeridos: imagen, peso o id_usuario'}), 400

    imagen_file = request.files['imagen']
    peso = request.form['peso']
    id_usuario = request.form['id_usuario']

    try:
        peso = float(peso)
        id_usuario = int(id_usuario)
    except ValueError:
        return jsonify({'error': 'Peso debe ser float e id_usuario un entero'}), 400

    # Guardar temporalmente la imagen como .jpg
    os.makedirs('static/tmp', exist_ok=True)
    nombre_archivo = f"{uuid.uuid4().hex}.jpg"
    ruta_destino = os.path.join('static/tmp', nombre_archivo)

    try:
        img = Image.open(imagen_file)
        rgb_im = img.convert('RGB')
        rgb_im.save(ruta_destino, format='JPEG')
        print("\n SE GUARDO \n")
    except Exception as e:
        return jsonify({'error': f'No se pudo procesar la imagen: {str(e)}'}), 500
    


    try:
        # Aquí clasifico el vegetal
        cambio = analizar_imagen(ruta_destino, peso, id_usuario)
    except Exception as e:
        pass
        #os.remove(ruta_destino)
        return jsonify({'error': f'Error en IA: {str(e)}'}), 500

    # Eliminar imagen después de usarla
    try:
        pass
        #os.remove(ruta_destino)
    except Exception:
        pass  # Si falla la eliminación, no es crítico

    if cambio.consumido:
        mensaje = "Se elimino un elemento del inventario"
    else:
        mensaje = "Se agrego un elemento del inventario"
    

    return jsonify({
        'mensaje': mensaje,
        'id': cambio.id,
        'vegetal': cambio.vegetal,
        'peso': cambio.peso,
        'usuario': cambio.id_usuario
    }), 201