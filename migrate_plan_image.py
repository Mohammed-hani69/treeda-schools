"""Add image column to plans table."""
import sqlite3
import sys
import os

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       'instance', 'school_exhibition.db')

if not os.path.exists(db_path):
    print(f'Database not found at {db_path}')
    sys.exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('PRAGMA table_info(plans)')
columns = [row[1] for row in cursor.fetchall()]

if 'image' not in columns:
    cursor.execute('ALTER TABLE plans ADD COLUMN image VARCHAR(255)')
    print('Added column: image')
else:
    print('image column already exists')

conn.commit()
conn.close()
print('Migration complete')
