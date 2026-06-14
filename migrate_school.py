"""Add category_id and image columns to schools table."""
from app import create_app, db

app = create_app()

with app.app_context():
    import sqlalchemy as sa
    inspector = sa.inspect(db.engine)
    columns = [c['name'] for c in inspector.get_columns('schools')]

    if 'image' not in columns:
        db.session.execute(sa.text('ALTER TABLE schools ADD COLUMN image VARCHAR(255)'))
        print('✅ Added column: image')
    else:
        print('ℹ️  Column image already exists')

    if 'category_id' not in columns:
        db.session.execute(sa.text('ALTER TABLE schools ADD COLUMN category_id INTEGER REFERENCES categories(id)'))
        print('✅ Added column: category_id')
    else:
        print('ℹ️  Column category_id already exists')

    db.session.commit()
    print('🎉 Migration complete')
