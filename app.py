from flask import Flask
import importlib
from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)

# Inicializace SQLAlchemy s aplikací
db.init_app(app)

def register_route(module_name, function_name, route, methods=['GET', 'POST']):
    module = importlib.import_module(f'routes.{module_name}')
    function = getattr(module, function_name)
    app.add_url_rule(route, view_func=function, methods=methods)

# Registrace rout pro kalendář
register_route('calendar_view', 'calendar_view', '/calendar/<int:year>/<int:month>')
register_route('day_view', 'day_view', '/day/<int:day>/<int:month>/<int:year>')

# Registrace rout pro události
register_route('event_list', 'event_list', '/events')
register_route('event_view', 'event_view', '/event/<int:event_id>')
register_route('event_edit', 'event_edit', '/event/edit/<int:event_id>', methods=['GET', 'POST'])
register_route('event_delete', 'event_delete', '/event/delete/<int:event_id>', methods=['POST'])
register_route('event_add', 'event_add', '/event/add', methods=['GET', 'POST'])

register_route('workshift_add', 'workshift_add', '/workshift/add')
register_route('workshift_edit', 'workshift_edit', '/workshift/edit/<int:workshift_id>')
register_route('workshift_delete', 'workshift_delete', '/workshift/delete/<int:workshift_id>', methods=['POST'])
register_route('workshifts_list', 'workshifts_list', '/workshifts')

register_route('workshifts_category_add', 'workshifts_category_add', '/workshift/category/add')
register_route('workshifts_category_edit', 'workshifts_category_edit', '/workshift/category/edit/<int:category_id>')
register_route('workshifts_category_delete', 'workshifts_category_delete', '/workshift/category/delete/<int:category_id>', methods=['GET', 'POST'])
register_route('workshifts_categories_list', 'workshifts_categories_list', '/workshifts/categories')

# Registrace rout pro kategorie
register_route('categories_list', 'categories_list', '/categories')
register_route('category_add', 'category_add', '/category/add', methods=['GET', 'POST'])
register_route('category_edit', 'category_edit', '/category/edit/<int:category_id>', methods=['GET', 'POST'])

# Registrace rout pro změnu stylu
register_route('change_theme', 'change_theme', '/change/theme')
register_route('set_theme', 'set_theme', '/set-theme', methods=['POST'])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
