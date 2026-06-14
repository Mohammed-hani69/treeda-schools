from datetime import datetime
from app import db


class Plan(db.Model):
    __tablename__ = 'plans'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='EGP')
    duration_days = db.Column(db.Integer, nullable=False)
    max_images = db.Column(db.Integer, default=10)
    max_videos = db.Column(db.Integer, default=5)
    storage_mb = db.Column(db.Integer, default=100)
    max_employees = db.Column(db.Integer, default=5)
    is_featured = db.Column(db.Boolean, default=False)
    image = db.Column(db.String(255))
    color = db.Column(db.String(20), default='#6366f1')
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    features = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    subscriptions = db.relationship('Subscription', backref='plan', lazy='dynamic')

    def get_features_list(self):
        if self.features:
            return [f.strip() for f in self.features.split('\n') if f.strip()]
        return []

    def __repr__(self):
        return f'<Plan {self.name} - {self.price}>'


class Subscription(db.Model):
    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='active')
    auto_renew = db.Column(db.Boolean, default=False)
    price_paid = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    payments = db.relationship('Payment', backref='subscription', lazy='dynamic')

    @property
    def is_expired(self):
        from datetime import datetime
        return datetime.utcnow() > self.end_date

    @property
    def days_remaining(self):
        from datetime import datetime
        delta = self.end_date - datetime.utcnow()
        return max(0, delta.days)

    def __repr__(self):
        return f'<Subscription School:{self.school_id} Plan:{self.plan_id}>'
