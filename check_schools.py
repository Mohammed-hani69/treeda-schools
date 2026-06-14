import sys
sys.path.insert(0, '.')
from app import create_app
app = create_app()
with app.test_client() as c:
    resp = c.get('/')
    h = resp.data.decode()
    for name in ['النخبة', 'المستقبل', 'المعرفة', 'أزهار', 'رواد', 'القمة']:
        ok = name in h
        print(f'  {"OK" if ok else "MISS"} {name}')
