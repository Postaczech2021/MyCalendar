from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Sdružovací tabulka pro vztahy mezi událostmi a štítky
event_badge_association = db.Table('event_badge_association',
    db.Column('event_id', db.Integer, db.ForeignKey('events.id'), primary_key=True),
    db.Column('badge_id', db.Integer, db.ForeignKey('events_badges.id'), primary_key=True)
)

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    events_category_id = db.Column(db.Integer, db.ForeignKey('events_category.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    done = db.Column(db.Boolean, default=False)
    category = db.relationship('EventCategory', back_populates='events')
    badges = db.relationship('EventBadge', secondary=event_badge_association, back_populates='events')

class EventCategory(db.Model):
    __tablename__ = 'events_category'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    events = db.relationship('Event', back_populates='category')

class EventBadge(db.Model):
    __tablename__ = 'events_badges'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    events = db.relationship('Event', secondary=event_badge_association, back_populates='badges')


class WorkshiftsCategory(db.Model):
    __tablename__ = 'workshifts_category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)

class Workshift(db.Model):
    __tablename__ = 'work_shifts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    time_start = db.Column(db.Time, nullable=False)
    time_end = db.Column(db.Time, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('workshifts_category.id'), nullable=False)
    category = db.relationship('WorkshiftsCategory', backref=db.backref('workshifts', lazy=True))
