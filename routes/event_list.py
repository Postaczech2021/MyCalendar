from . import *

def event_list():
    events = Event.query.all()
    current_year = datetime.now().year
    current_month_number = datetime.now().month

    theme = request.cookies.get('theme', 'dark')

    return render_template('event_list.html', events=events, current_year=current_year, current_month_number=current_month_number, theme=theme)
