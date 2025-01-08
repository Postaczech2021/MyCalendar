from . import *

def event_add():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description')
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%dT%H:%M')
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%dT%H:%M')
        
        # Validace
        if start_date > end_date:
            flash('Čas začátku události nemůže být vyšší než čas konce události.', 'danger')
            categories = EventCategory.query.all()
            return render_template('event_add.html', categories=categories)

        category_id = request.form.get('category_id', None)
        if category_id is None:
            category = EventCategory.query.filter_by(name='Undefined').first()
            category_id = category.id

        new_event = Event(name=name, description=description, start_date=start_date, end_date=end_date, events_category_id=category_id)
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('event_list'))

    categories = EventCategory.query.all()
    current_year = datetime.now().year
    current_month_number = datetime.now().month
    theme = request.cookies.get('theme', 'dark')
    return render_template('event_add.html', categories=categories, current_year=current_year, current_month_number=current_month_number, theme=theme)
