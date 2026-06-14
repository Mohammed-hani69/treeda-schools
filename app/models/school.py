from datetime import datetime
from app import db


class School(db.Model):
    __tablename__ = 'schools'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    name_en = db.Column(db.String(200))
    about = db.Column(db.Text)
    address = db.Column(db.String(300))
    city = db.Column(db.String(100))
    district = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    phone2 = db.Column(db.String(20))
    email = db.Column(db.String(120))
    website = db.Column(db.String(200))
    logo = db.Column(db.String(255))
    cover = db.Column(db.String(255))
    image = db.Column(db.String(255))
    school_type = db.Column(db.String(50))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    gender = db.Column(db.String(20))
    founded_year = db.Column(db.Integer)
    facebook = db.Column(db.String(255))
    twitter = db.Column(db.String(255))
    instagram = db.Column(db.String(255))
    youtube = db.Column(db.String(255))
    whatsapp = db.Column(db.String(20))
    telegram = db.Column(db.String(255))
    map_lat = db.Column(db.Float)
    map_lng = db.Column(db.Float)
    is_featured = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    media = db.relationship('SchoolMedia', backref='school', lazy='dynamic', cascade='all, delete-orphan')
    activities = db.relationship('SchoolActivity', backref='school', lazy='dynamic', cascade='all, delete-orphan')
    services = db.relationship('SchoolService', backref='school', lazy='dynamic', cascade='all, delete-orphan')
    grades = db.relationship('SchoolGrade', backref='school', lazy='dynamic', cascade='all, delete-orphan')
    subscription = db.relationship('Subscription', backref='school', uselist=False, lazy=True)

    def storage_used_mb(self):
        total = sum(
            m.file_size or 0
            for m in self.media.all()
        )
        return total / (1024 * 1024)

    def media_count_by_type(self, media_type):
        return self.media.filter_by(media_type=media_type).count()

    def approved_media(self, media_type=None):
        q = self.media.filter_by(status='approved')
        if media_type:
            q = q.filter_by(media_type=media_type)
        return q

    def get_counts(self):
        counts = {'image': 0, 'video': 0, 'pending': 0, 'total': 0}
        for m in self.media.all():
            counts['total'] += 1
            counts[m.media_type] = counts.get(m.media_type, 0) + 1
            if m.status == 'pending':
                counts['pending'] += 1
        return counts

    def __repr__(self):
        return f'<School {self.name}>'


class SchoolVisitLog(db.Model):
    __tablename__ = 'school_visit_logs'

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    visits = db.Column(db.Integer, default=0)
    unique_visitors = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    school = db.relationship('School', backref='visit_logs', lazy=True)

    @classmethod
    def record_visit(cls, school_id, ip_address=None):
        from datetime import date
        today = date.today()
        log = cls.query.filter_by(school_id=school_id, date=today).first()
        if not log:
            log = cls(school_id=school_id, date=today, visits=0, unique_visitors=0)
            db.session.add(log)
        log.visits += 1
        return log

    def __repr__(self):
        return f'<VisitLog school={self.school_id} date={self.date} visits={self.visits}>'


class SchoolMedia(db.Model):
    __tablename__ = 'school_media'

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False, index=True)
    media_type = db.Column(db.String(10), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    original_name = db.Column(db.String(255))
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending', index=True)
    rejection_reason = db.Column(db.Text)
    is_featured = db.Column(db.Boolean, default=False)
    file_size = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Media {self.filename} - {self.status}>'


class SchoolActivity(db.Model):
    __tablename__ = 'school_activities'

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))
    image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class SchoolService(db.Model):
    __tablename__ = 'school_services'

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class SchoolGrade(db.Model):
    __tablename__ = 'school_grades'

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
