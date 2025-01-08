from . import *

def event_view(event_id):
    event = Event.query.get(event_id)
    if not event:
        return redirect(url_for('event_list'))

    theme = request.cookies.get('theme', 'dark')

    return render_template('event_view.html', event=event, theme=theme)
