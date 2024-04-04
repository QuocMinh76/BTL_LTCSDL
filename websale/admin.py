from websale import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, AdminIndexView
from websale.models import Category, Product, UserRole
from flask_login import current_user, logout_user
from flask import redirect
import utils

class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)

class ProductView(AuthenticatedModelView):
    column_list = ['name', 'description', 'price', 'category']
    column_searchable_list = ['name', 'description']
    column_filters = ['name', 'price']
    column_sortable_list = ['name', 'price']
    can_export = True
    can_view_details = True


class CategoryView(AuthenticatedModelView):
    column_list = ['name', 'products']


class LogoutView(BaseView):
    @expose('/')
    def __index__(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated\


class MyAdminIndex(AdminIndexView):
    @expose('/')
    def __index__(self):
        return self.render('admin/index.html',
                           stats=utils.category_stats())

admin = Admin(app=app,
              name="E-commerce Administration",
              template_mode='bootstrap4',
              index_view=MyAdminIndex())
admin.add_view(CategoryView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(LogoutView(name='Logout'))