from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    db.create_all()

    if not User.query.filter_by(role='admin').first():
        admin = User(
            username='admin',
            email='admin@treeda.com',
            role='admin',
            is_active=True,
            is_verified=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('✅ Admin account created successfully!')
    else:
        print('ℹ️  Admin account already exists.')

    print('📧 Admin login: admin@treeda.com')
    print('🔑 Admin password: admin123')
