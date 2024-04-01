from websale import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from websale.models import Category, Product

admin = Admin(app=app, name="E-commerce Administration", template_mode='bootstrap4')

class ProductView(ModelView):
    column_list = ['name', 'description', 'price', 'category']
    column_searchable_list = ['name', 'description']
    column_filters = ['name', 'price']
    column_sortable_list = ['name', 'price']
    can_export = True
    can_view_details = True


class CategoryView(ModelView):
    column_list = ['name', 'products']


admin.add_view(CategoryView(Category, db.session))
admin.add_view(ProductView(Product, db.session))