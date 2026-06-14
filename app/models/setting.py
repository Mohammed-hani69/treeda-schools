from datetime import datetime
from app import db


class Setting(db.Model):
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    site_name = db.Column(db.String(200), default='المعرض الإلكتروني للمدارس')
    site_name_en = db.Column(db.String(200), default='School Exhibition')
    site_description = db.Column(db.Text)
    logo = db.Column(db.String(255))
    favicon = db.Column(db.String(255))
    contact_email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(20))
    address = db.Column(db.String(300))
    facebook = db.Column(db.String(255))
    twitter = db.Column(db.String(255))
    instagram = db.Column(db.String(255))
    youtube = db.Column(db.String(255))
    whatsapp = db.Column(db.String(20))
    theme = db.Column(db.String(10), default='light')
    primary_color = db.Column(db.String(20), default='#6366f1')
    secondary_color = db.Column(db.String(20), default='#ec4899')
    font_family = db.Column(db.String(100), default='Cairo')
    currency = db.Column(db.String(10), default='EGP')
    maintenance_mode = db.Column(db.Boolean, default=False)
    bank_transfer_number = db.Column(db.String(100), default='100051892245')
    instapay_phone = db.Column(db.String(20), default='01001406922')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Setting {self.site_name}>'
