from flask import Flask

from send import send

# Creamos una instancia de la aplicación Flask
app = Flask(__name__)

# Declaramos un endpoint para la ruta raíz '/'
@app.route('/')
def index():
    return '¡Hola, mundo! Este es el endpoint raíz.'

# Declaramos un endpoint para la ruta '/saludo/<nombre>'
@app.route('/send', methods=['POST'])
def send_message():
    return send()

if __name__ == '__main__':
    # Ejecutamos la aplicación Flask en el servidor local en el puerto 5000
    app.run(debug=True)