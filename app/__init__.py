from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import config


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # import routes
        from routes.campaign_routes import campaign_bp
        from routes.player_routes import player_bp
        # register blueprints
        app.register_blueprint(campaign_bp)
        app.register_blueprint(player_bp)

        return app