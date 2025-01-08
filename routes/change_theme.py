from . import *

def change_theme():
    current_year = datetime.now().year
    current_month_number = datetime.now().month

    theme = request.cookies.get('theme', 'dark')

    return render_template('change_theme.html', current_year=current_year, current_month_number=current_month_number, theme=theme)
