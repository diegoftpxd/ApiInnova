from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
from models import Inventario


model = YOLO("best.pt")


def analizar_imagen(ruta_imagen, peso, id_usuario):

    # Se saca algo
    if peso < 0:
        return retiro_de_vegetal(ruta_imagen, peso, id_usuario)
    if peso >= 0:
        return agregar_vegetal(ruta_imagen, peso, id_usuario)




def retiro_de_vegetal(ruta_imagen, peso, id_usuario):

    lista_vegetales = mas_probable(ruta_imagen)
    for candidato in lista_vegetales:
        if peso_razonable(candidato, peso):
            try:
                return  Inventario.marcar_como_consumido_por_vegetal_y_peso(id_usuario, candidato, peso)            
            except ValueError as e:
                print(e)
    raise ValueError("Dentro de la imagen no se pudo detectar ningún vegetal con un peso razonable")

def agregar_vegetal(ruta_imagen, peso, id_usuario):
    lista_vegetales = mas_probable(ruta_imagen)
    for candidato in lista_vegetales:
        if peso_razonable(candidato, peso):
            try:
                return Inventario.crear(id_usuario, candidato, peso, 0, False)     
            except ValueError as e:
                print(e)
    raise ValueError("Dentro de la imagen no se pudo detectar ningún vegetal con un peso razonable")




# Función que toma una imagen y te dice que vegetales hay, enterga una lista ordenada por confianza
def mas_probable(ruta_imagen):
    results = model(ruta_imagen, save=False)

    # Extraer todas las detecciones válidas como (confianza, etiqueta)
    detecciones = [
        (float(box.conf), model.names[int(box.cls)])
        for result in results
        for box in result.boxes
    ]

    if not detecciones:
        return []  # No se detectó nada

    # Ordenar por confianza descendente
    detecciones_ordenadas = sorted(detecciones, key=lambda x: x[0], reverse=True)

    # Traducir las etiquetas al español
    etiquetas_traducidas = [traducir_a_espanol(etiqueta) for _, etiqueta in detecciones_ordenadas]

    print(f"Orden de predicción: {etiquetas_traducidas}")
    return etiquetas_traducidas



# Cambia el nombre a español
def traducir_a_espanol(nombre_ingles):
    traducciones = {
        'apple': 'Manzana',
        'avocado': 'Palta',
        'banana': 'Plátano',
        'beans': 'Porotos',
        'blackberrie': 'Mora',
        'cabbage': 'Repollo',
        'cactus': 'Cactus',
        'caju': 'Cajú',
        'carrot': 'Zanahoria',
        'cherimoya': 'Chirimoya',
        'cucumber': 'Pepino',
        'eggplant': 'Berenjena',
        'gooseberry': 'Grosella',
        'pear': 'Pera',
        'pistachio': 'Pistacho',
        'quince': 'Membrillo',
        'tomato': 'Tomate',
        'zucchini': 'Zapallito italiano',
        'cherry': 'Cereza'
    }
    
    return traducciones.get(nombre_ingles, nombre_ingles.capitalize())



# Si el peso es un peso razonable para esa verdura se queda
def peso_razonable(vegetal, peso):
    pesos = {
        'Manzana': (0.1, 0.4),
        'Palta': (0.1, 0.3),
        'Plátano': (0.1, 0.3),
        'Porotos': (0.05, 1.0),
        'Mora': (0.05, 0.5),
        'Repollo': (0.5, 2.5),
        'Cactus': (0.2, 3.0),
        'Cajú': (0.01, 0.3),
        'Zanahoria': (0.05, 0.3),
        'Chirimoya': (0.2, 0.7),
        'Pepino': (0.2, 0.6),
        'Berenjena': (0.2, 0.7),
        'Grosella': (0.05, 0.5),
        'Pera': (0.1, 0.3),
        'Pistacho': (0.01, 0.5),
        'Membrillo': (0.2, 0.5),
        'Tomate': (0.05, 0.4),
        'Zapallito Italiano': (0.2, 0.7),
        'Cereza': (0.01, 0.2)
    }
    
    inf = pesos[vegetal][0]
    sup = pesos[vegetal][1]
    if inf <= abs(peso) <= sup:
        return True
    else:
        return False