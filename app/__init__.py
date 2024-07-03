from flask import Flask, render_template
from app.routes.register_routes import register_bp
from app.routes.login_routes import login_bp
from app.routes.inventory_routes import inventory_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'  # Asegúrate de tener una clave secreta segura

    # Importar Blueprints y registrarlos
    from app.routes.login_routes import login_bp
    from app.routes.register_routes import register_bp
    from app.routes.inventory_routes import inventory_bp

    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(inventory_bp)
    
    @app.route('/')
    def home():
        return render_template('index.html')

    return app