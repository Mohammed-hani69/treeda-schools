from datetime import datetime
from flask import current_app, session, request
from app.models.setting import Setting
from app.utils.translations import _ as _tr

def get_lang():
    lang = request.args.get('lang') if request else None
    if lang in ('en', 'ar'):
        session['lang'] = lang
    return session.get('lang', 'en')

def inject_globals(app):
    @app.context_processor
    def inject():
        setting = Setting.query.first()
        if not setting:
            setting = Setting()
            from app import db
            db.session.add(setting)
            db.session.commit()
        current_lang = get_lang()

        def _(key):
            return _tr(key, current_lang)

        site_name = setting.site_name_en if current_lang == 'en' and setting.site_name_en else setting.site_name or 'المعرض الإلكتروني للمدارس'
        currency = setting.currency or 'EGP'

        return {
            'setting': setting,
            'site_name': site_name,
            'currency': currency,
            'now': datetime.now,
            '_': _,
            'current_lang': current_lang,
        }