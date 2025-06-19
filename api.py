from flask import Flask
from models import db
from routes.inventario import inventario_bp
from routes.dispositivo import dispositivo_bp


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Registrar blueprint
app.register_blueprint(inventario_bp)
app.register_blueprint(dispositivo_bp)


@app.route('/')
def inicio():
    return "Hello world"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
