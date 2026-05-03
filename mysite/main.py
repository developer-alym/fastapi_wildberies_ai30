from fastapi import FastAPI
from api import user, category, sub_category, auth
from admin.setup import setup_admin

wildberies_app = FastAPI(title='FastAPI Wildberies ai-30')

wildberies_app.include_router(user.user_router)
wildberies_app.include_router(category.category_router)
wildberies_app.include_router(sub_category.sub_category_router)
wildberies_app.include_router(auth.auth_router)

setup_admin(wildberies_app)








































