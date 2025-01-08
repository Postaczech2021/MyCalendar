from . import *

def event_edit(event_id):
    event = Event.query.get_or_404(event_id)

    if request.method == 'POST':
        event.name = request.form['name']
        event.description = request.form['description']
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%dT%H:%M')
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%dT%H:%M')
        
        # Validace
        if start_date > end_date:
            flash('Čas začátku události nemůže být vyšší než čas konce události.', 'danger')
            categories = EventCategory.query.all()
            return render_template('event_edit.html', event=event, categories=categories)

        event.start_date = start_date
        event.end_date = end_date
        event.events_category_id = request.form['category_id']
        event.done = 'done' in request.form
        db.session.commit()
        return redirect(url_for('event_view', event_id=event.id))

    categories = EventCategory.query.all()
    theme = request.cookies.get('theme', 'dark')
    return render_template('event_edit.html', event=event, categories=categories, theme=theme)
