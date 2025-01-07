from models import db, Event, EventCategory, EventBadge

class Events:
    def __init__(self):
        pass

    def add_event(self, name, description, category_id, start_date, end_date, done=False):
        """
        Přidá novou událost do databáze.
        """
        new_event = Event(
            name=name,
            description=description,
            events_category_id=category_id,
            start_date=start_date,
            end_date=end_date,
            done=done
        )
        db.session.add(new_event)
        db.session.commit()
        return new_event

    def edit_event(self, event_id, name=None, description=None, category_id=None, start_date=None, end_date=None, done=None):
        """
        Upraví existující událost v databázi.
        """
        event = Event.query.get(event_id)
        if event:
            if name:
                event.name = name
            if description:
                event.description = description
            if category_id:
                event.events_category_id = category_id
            if start_date:
                event.start_date = start_date
            if end_date:
                event.end_date = end_date
            if done is not None:
                event.done = done
            db.session.commit()
        return event

    def delete_event(self, event_id):
        """
        Smaže existující událost z databáze.
        """
        event = Event.query.get(event_id)
        if event:
            db.session.delete(event)
            db.session.commit()
        return event

    def get_event_by_id(self, event_id):
        """
        Načte událost z databáze podle ID.
        """
        return Event.query.get(event_id)

    def get_all_events(self):
        """
        Načte všechny události z databáze.
        """
        return Event.query.all()
