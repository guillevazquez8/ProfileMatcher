from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger
from config import config


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    Swagger(app, template={
        "info": {
            "title": "Profile Matcher API",
            "description": "A profile matcher for video games",
            "version": "1.0.0"
        }
    })

    with app.app_context():
        # import routes
        from app.routes.campaign_routes import campaign_bp
        from app.routes.player_routes import player_bp
        # register blueprints
        app.register_blueprint(campaign_bp)
        app.register_blueprint(player_bp)

        return app