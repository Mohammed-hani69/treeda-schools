from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_caching import Cache
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()
cache = Cache()

login_manager.login_view = 'auth.login'
login_manager.login_message = 'يرجى تسجيل الدخول أولاً'
login_manager.login_message_category = 'warning'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['UPLOAD_FOLDER'] = config_class.UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = config_class.MAX_CONTENT_LENGTH

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    cache.init_app(app)

    from app.models.user import User
    from app.models.school import School, SchoolMedia, SchoolActivity, SchoolService, SchoolGrade
    from app.models.parent import Parent
    from app.models.plan import Plan, Subscription
    from app.models.category import Category
    from app.models.home import HomeSection, HeroSection
    from app.models.notification import Notification
    from app.models.payment import Payment
    from app.models.setting import Setting

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.school_routes import school_bp
    from app.routes.parent_routes import parent_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.api_routes import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(school_bp, url_prefix='/school')
    app.register_blueprint(parent_bp, url_prefix='/parent')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api')

    with app.app_context():
        from app.utils.context_processors import inject_globals
        inject_globals(app)

    return app
