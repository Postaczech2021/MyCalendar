from flask import Flask, render_template, request, redirect, url_for
from calendar_class import Calendar
from models import Event
from datetime import datetime

app = Flask(__name__)

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

    theme = request.cookies.get('theme', 'dark')

    return render_template('calendar.html', 
                           year=year, 
                           month=month, 
                           prev_year=prev_year,
                           prev_month=prev_month,
                           next_year=next_year,
                           next_month=next_month,
                           current_month=current_month, 
                           cz_abbr_days=cz_abbr_days, 
                           days_matrix=days_matrix,
                           theme=theme)

@app.route('/day/<int:day>/<int:month>/<int:year>')
def day_view(day, month, year):
    """
    Zobrazí detailní informace o daném dni včetně událostí.
    """
    events = Event.query.filter_by(start_date=datetime(year, month, day)).all()
    current_year = datetime.now().year
    current_month_number = datetime.now().month

    theme = request.cookies.get('theme', 'dark')

    return render_template('day.html', day=day, month=month, year=year, events=events, current_year=current_year, current_month_number=current_month_number, theme=theme)

@app.route('/change/theme')
def change_theme():
    """
    Zobrazí formulář pro změnu stylu.
    """
    current_year = datetime.now().year
    current_month_number = datetime.now().month

    theme = request.cookies.get('theme', 'dark')

    return render_template('change_theme.html', current_year=current_year, current_month_number=current_month_number, theme=theme)

@app.route('/set-theme', methods=['POST'])
def set_theme():
    """
    Nastaví vybraný styl a uloží jej do cookies.
    """
    theme = request.form.get('theme')
    response = redirect(request.referrer)
    response.set_cookie('theme', theme)
    return response

if __name__ == '__name__':
    app.run(debug=True)
