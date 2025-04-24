from flask import Flask

def create_app():
    """Flask uygulamasını oluşturur ve yapılandırır."""
    app = Flask(__name__)
    
    # Rotaları kaydet
    from app import routes
    app.register_blueprint(routes.main)
    
    return app 