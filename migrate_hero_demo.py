"""Add demo_video column to hero_sections table."""
import sqlite3
import sys
import os

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       'instance', 'school_exhibition.db')

if not os.path.exists(db_path):
    print(f'❌ Database not found at {db_path}')
    sys.exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('PRAGMA table_info(hero_sections)')
columns = [row[1] for row in cursor.fetchall()]

if 'demo_video' not in columns:
    cursor.execute('ALTER TABLE hero_sections ADD COLUMN demo_video VARCHAR(255)')
    print('✅ Added column: demo_video')
else:
    print('ℹ️  demo_video column already exists')

conn.commit()
conn.close()
print('🎉 Migration complete')
