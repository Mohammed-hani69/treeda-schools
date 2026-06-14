import sqlite3, os
db = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'school_exhibition.db')
conn = sqlite3.connect(db)
cur = conn.cursor()
cur.execute('SELECT id, name, is_featured, is_approved, is_active FROM schools')
rows = cur.fetchall()
for r in rows:
    print(f'ID:{r[0]} | "{r[1]}" | featured={r[2]} | approved={r[3]} | active={r[4]}')
if not rows:
    print('No schools found')
conn.close()
