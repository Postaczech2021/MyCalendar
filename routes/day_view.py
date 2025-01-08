from . import *

def day_view(day, month, year):
    selected_date = datetime(year, month, day).date()
    
    # Načteme všechny události
    all_events = Event.query.all()
    
    # Filtrujeme pouze ty události, které odpovídají zvolenému datu
    events = [event for event in all_events if event.start_date.date() <= selected_date <= event.end_date.date()]

    current_year = datetime.now().year
    current_month_number = datetime.now().month
    theme = request.cookies.get('theme', 'dark')
    day_name = Calendar.get_day_name(selected_date)

    return render_template('day.html', 
                           day=day, 
                           month=month, 
                           year=year, 
                           day_name=day_name, 
                           events=events, 
                           current_year=current_year, 
                           current_month_number=current_month_number, 
                           theme=theme)
