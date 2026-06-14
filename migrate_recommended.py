"""Add is_recommended column to schools table."""
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

cursor.execute('PRAGMA table_info(schools)')
columns = [row[1] for row in cursor.fetchall()]

if 'is_recommended' not in columns:
    cursor.execute('ALTER TABLE schools ADD COLUMN is_recommended BOOLEAN DEFAULT 0')
    print('✅ Added column: is_recommended')
else:
    print('ℹ️  is_recommended already exists')

conn.commit()
conn.close()
print('🎉 Migration complete')
