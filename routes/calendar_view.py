from . import *

def calendar_view(year, month):
    calendar = Calendar(year, month)
    prev_year, prev_month = calendar.get_prev_month()
    next_year, next_month = calendar.get_next_month()
    current_month = calendar.get_current_month_name()
    cz_abbr_days = calendar.get_cz_abbr_days()
    days_matrix = calendar.get_days_matrix()
    current_day = datetime.now().date()

    events_by_day = {}
    events = Event.query.filter(
        Event.start_date <= datetime(year, month, calendar.get_days_in_month()).date(),
        Event.end_date >= datetime(year, month, 1).date()
    ).all()
    for event in events:
        start_date = event.start_date.date()
        end_date = event.end_date.date()
        current_date = start_date
        while current_date <= end_date:
            if current_date.year == year and current_date.month == month:
                events_by_day.setdefault(current_date.day, 0)
                events_by_day[current_date.day] += 1
            current_date += timedelta(days=1)

    recent_events = Event.query.order_by(Event.start_date.desc()).limit(5).all()

    theme = request.cookies.get('theme', 'dark')

    return render_template('calendar.html', 
                           year=year, 
                           month=month, 
                           datetime=datetime,
                           prev_year=prev_year,
                           prev_month=prev_month,
                           next_year=next_year,
                           next_month=next_month,
                           current_month=current_month, 
                           cz_abbr_days=cz_abbr_days, 
                           days_matrix=days_matrix,
                           current_day=current_day,
                           events_by_day=events_by_day,
                           recent_events=recent_events,
                           theme=theme)
