"""Add missing columns to schools table for production."""
import sqlite3
import sys
import os

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'treeda.db')

if not os.path.exists(db_path):
    print(f'❌ Database not found at {db_path}')
    sys.exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check existing columns
cursor.execute('PRAGMA table_info(schools)')
columns = [row[1] for row in cursor.fetchall()]

if 'image' not in columns:
    cursor.execute('ALTER TABLE schools ADD COLUMN image VARCHAR(255)')
    print('✅ Added column: image')
else:
    print('ℹ️  image column already exists')

if 'category_id' not in columns:
    cursor.execute('ALTER TABLE schools ADD COLUMN category_id INTEGER REFERENCES categories(id)')
    print('✅ Added column: category_id')
else:
    print('ℹ️  category_id column already exists')

conn.commit()
conn.close()
print('🎉 Migration complete')
