from datetime import datetime
from app import db


class AiKnowledge(db.Model):
    __tablename__ = 'ai_knowledge'

    id = db.Column(db.Integer, primary_key=True)
    keywords = db.Column(db.Text, nullable=False)
    answer_ar = db.Column(db.Text, nullable=False)
    answer_en = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default='general')
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_keywords_list(self):
        return [k.strip().lower() for k in self.keywords.split(',') if k.strip()]

    def __repr__(self):
        return f'<AiKnowledge {self.id}: {self.keywords[:30]}>'
