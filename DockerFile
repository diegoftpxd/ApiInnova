# Usamos una imagen base oficial de Python
FROM python:3.10-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo de dependencias (crea uno si no tienes)
COPY requirements.txt .

# Instalamos dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos TODO el contenido del proyecto al contenedor
COPY . .

# Exponemos el puerto 4001 para que sea accesible desde fuera
EXPOSE 4001

# Comando para arrancar la app Flask
# Asegúrate que api.py lance la app en host=0.0.0.0 y puerto 4001
CMD ["python", "api.py"]
