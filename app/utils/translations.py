import json
import os

TR_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'translations', 'en.json')
_tr_cache = {}
_tr_mtime = 0

def _load():
    global _tr_mtime
    try:
        mtime = os.path.getmtime(TR_PATH)
        if mtime > _tr_mtime:
            with open(TR_PATH, encoding='utf-8') as f:
                _tr_cache.clear()
                _tr_cache.update(json.load(f))
            _tr_mtime = mtime
    except Exception:
        pass

def _nested_get(data, key):
    keys = key.split('.')
    for k in keys:
        if isinstance(data, dict):
            data = data.get(k)
            if data is None:
                return None
        elif isinstance(data, list):
            try:
                idx = int(k)
                data = data[idx]
            except (ValueError, IndexError):
                return None
        else:
            return None
    return data

def _(key, lang='ar'):
    _load()
    if not _tr_cache:
        return key
    val = _nested_get(_tr_cache, key)
    if isinstance(val, dict) and 'ar' in val and 'en' in val:
        return val.get(lang, val.get('ar', key))
    if isinstance(val, str):
        return val
    return val if val is not None else key

_load()
