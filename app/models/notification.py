from datetime import datetime
from app import db


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text)
    notification_type = db.Column(db.String(50))
    link = db.Column(db.String(255))
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    NOTIFICATION_TYPES = {
        'content_approved': 'قبول المحتوى',
        'content_rejected': 'رفض المحتوى',
        'subscription_expired': 'انتهاء الاشتراك',
        'subscription_soon': 'اقتراب انتهاء الاشتراك',
        'admin_message': 'رسالة من الأدمن',
        'school_registered': 'تسجيل مدرسة جديدة',
        'parent_registered': 'تسجيل ولي أمر جديد',
    }

    def __repr__(self):
        return f'<Notification {self.notification_type} - Read:{self.is_read}>'
