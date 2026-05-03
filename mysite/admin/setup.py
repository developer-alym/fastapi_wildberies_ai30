from fastapi import FastAPI
from sqladmin import Admin
from db.database import engine
from .view import (UserProfileView, CategoryView,
                   SubCategoryView)

def setup_admin(app: FastAPI):
    admin = Admin(app, engine=engine)
    admin.add_view(UserProfileView)
    admin.add_view(CategoryView)
    admin.add_view(SubCategoryView)








