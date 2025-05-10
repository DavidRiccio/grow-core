# Usa la imagen base de Python
FROM python:3.11

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de la aplicación al contenedor
COPY . /app/

# Instala las dependencias
RUN pip install -r requirements.txt

# Expón el puerto 8000
EXPOSE 8000

# Ejecuta el servidor de desarrollo de Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
