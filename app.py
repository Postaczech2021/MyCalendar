from flask import Flask, render_template, redirect, url_for, request
from models import db, Event, EventCategory, EventBadge
from events import Events
from forms import EventForm
from datetime import datetime,timedelta
from calendar_class import Calendar

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ghhgg676678bhghj86ugbh'  # Přidán tajný klíč pro CSRF ochranu
db.init_app(app)

events_service = Events()

def get_theme():
    """
    Získá aktuální téma z cookies.
    """
    return request.cookies.get('theme', 'dark')

@app.route('/calendar/<int:year>/<int:month>')
def calendar_view(year, month):
    """
    Zobrazí kalendář pro daný rok a měsíc.
    """
    calendar = Calendar(year, month)
    prev_year, prev_month = calendar.get_prev_month()
    next_year, next_month = calendar.get_next_month()
    current_month = calendar.get_current_month_name()
    cz_abbr_days = calendar.get_cz_abbr_days()
    days_matrix = calendar.get_days_matrix()
    current_day = datetime.now()
    current_day_info = calendar.get_current_day_info()
    recent_events = Event.query.order_by(Event.start_date.desc()).limit(5).all()

    theme = get_theme()

    return render_template('calendar.html', 
                           year=year, 
                           month=month, 
                           recent_events=recent_events,
                           current_day=current_day,
                           prev_year=prev_year,
                           prev_month=prev_month,
                           next_year=next_year,
                           next_month=next_month,
                           current_month=current_month, 
                           cz_abbr_days=cz_abbr_days, 
                           days_matrix=days_matrix,
                           theme=theme,
                           cdi=current_day_info)


@app.route('/day/<int:day>/<int:month>/<int:year>')
def day_view(day, month, year):
    """
    Zobrazí detailní informace o daném dni včetně událostí
    """
    # Vytvoření datumu ve formátu "d.m.Y"
    selected_date_str = f"{day}.{month}.{year}"
    selected_date = datetime.strptime(selected_date_str, '%d.%m.%Y').date()

    # Výběr všech událostí pro daný den
    events = Event.query.filter(
        db.func.date(Event.start_date) == selected_date,
        db.func.date(Event.end_date) == selected_date
    ).all()

    # Získání názvu dne v týdnu v češtině
    calendar = Calendar(year, month)
    cz_abbr_days = calendar.get_cz_abbr_days()
    day_name = cz_abbr_days[selected_date.weekday()]

    theme = get_theme()

    return render_template('day.html', day=day, month=month, year=year, day_name=day_name, events=events, theme=theme)
@app.route('/change/theme')
def change_theme():
    """
    Zobrazí formulář pro změnu stylu.
    """
    theme = get_theme()

    return render_template('change_theme.html', theme=theme,datetime=datetime)

@app.route('/set-theme', methods=['POST'])
def set_theme():
    """
    Nastaví vybraný styl a uloží jej do cookies.
    """
    theme = request.form.get('theme')
    response = redirect(url_for('calendar_view', year=datetime.now().year, month=datetime.now().month))
    response.set_cookie('theme', theme)
    return response

@app.route('/events')
def events_list():
    print("Accessing events list")
    all_events = events_service.get_all_events()
    return render_template('events_list.html', events=all_events)

@app.route('/event/add', methods=['GET', 'POST'])
def add_event():
    form = EventForm()
    if form.validate_on_submit():
        print("Form validated successfully")
        
        # Převod formátu "d.m.Y" na objekt datetime
        try:
            start_date = datetime.strptime(form.start_date.data, '%d.%m.%Y')
            end_date = datetime.strptime(form.end_date.data, '%d.%m.%Y')
        except ValueError as e:
            print(f"Error parsing dates: {e}")
            return render_template('event_add.html', form=form, date_error="Nesprávný formát data. Použijte formát d.m.Y")

        events_service.add_event(
            name=form.name.data,
            description=form.description.data,
            category_id=form.category.data,
            start_date=start_date,
            end_date=end_date,
            done=form.done.data
        )
        return redirect(url_for('events_list'))
    else:
        if request.method == 'POST':
            print("Form validation failed")
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Error in {field}: {error}")
    return render_template('event_add.html', form=form)        
    
from datetime import datetime

@app.route('/event/edit/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    event = events_service.get_event_by_id(event_id)
    if not event:
        return redirect(url_for('events_list'))

    form = EventForm(obj=event)
    if form.validate_on_submit():
        try:
            start_date = datetime.strptime(form.start_date.data, '%d.%m.%Y')
            end_date = datetime.strptime(form.end_date.data, '%d.%m.%Y')
        except ValueError as e:
            print(f"Error parsing dates: {e}")
            return render_template('event_edit.html', form=form, event_id=event_id, date_error="Nesprávný formát data. Použijte formát d.m.Y")

        events_service.edit_event(
            event_id=event_id,
            name=form.name.data,
            description=form.description.data,
            category_id=form.category.data,
            start_date=start_date,
            end_date=end_date,
            done=form.done.data
        )
        return redirect(url_for('events_list'))
    else:
        if request.method == 'POST':
            print("Form validation failed")
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Error in {field}: {error}")

    # Převedení dat pro zobrazení ve formátu "d.m.Y"
    if form.start_date.data:
        form.start_date.data = form.start_date.data.strftime('%d.%m.%Y')
    if form.end_date.data:
        form.end_date.data = form.end_date.data.strftime('%d.%m.%Y')

    return render_template('event_edit.html', form=form, event_id=event_id)
    
@app.route('/event/delete/<int:event_id>')
def delete_event(event_id):
    events_service.delete_event(event_id)
    return redirect(url_for('events_list'))

@app.route('/categories', methods=['GET', 'POST'])
def manage_categories():
    if request.method == 'POST':
        category_name = request.form.get('category_name')
        new_category = EventCategory(name=category_name)
        db.session.add(new_category)
        db.session.commit()
        return redirect(url_for('manage_categories'))

    categories = EventCategory.query.all()
    return render_template('manage_categories.html', categories=categories)

@app.route('/category/edit/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    category = EventCategory.query.get(category_id)
    if not category:
        return redirect(url_for('manage_categories'))

    if request.method == 'POST':
        category_name = request.form.get('category_name')
        category.name = category_name
        db.session.commit()
        return redirect(url_for('manage_categories'))

    return render_template('edit_category.html', category=category)

@app.route('/category/delete/<int:category_id>')
def delete_category(category_id):
    category = EventCategory.query.get(category_id)
    if category:
        db.session.delete(category)
        db.session.commit()
    return redirect(url_for('manage_categories'))

@app.route('/badges', methods=['GET', 'POST'])
def manage_badges():
    if request.method == 'POST':
        badge_name = request.form.get('badge_name')
        new_badge = EventBadge(name=badge_name)
        db.session.add(new_badge)
        db.session.commit()
        return redirect(url_for('manage_badges'))

    badges = EventBadge.query.all()
    return render_template('manage_badges.html', badges=badges)

@app.route('/badge/edit/<int:badge_id>', methods=['GET', 'POST'])
def edit_badge(badge_id):
    badge = EventBadge.query.get(badge_id)
    if not badge:
        return redirect(url_for('manage_badges'))

    if request.method == 'POST':
        badge_name = request.form.get('badge_name')
        badge.name = badge_name
        db.session.commit()
        return redirect(url_for('manage_badges'))

    return render_template('edit_badge.html', badge=badge)

@app.route('/badge/delete/<int:badge_id>')
def delete_badge(badge_id):
    badge = EventBadge.query.get(badge_id)
    if badge:
        db.session.delete(badge)
        db.session.commit()
    return redirect(url_for('manage_badges'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)    
