1. pip install fastapi
2. mysity/
            admin/
            api/
            db/
3. db/ database.py
       models.py
       schema.py
4. db/ databse.py -> sqlalchemy(DB + FastAPI(Backend))
5. db/ models.py
6. db/ schema.py -> validation + json
7. alembic -> migration(models.py) -> ORM
8. CRUD -> (api/ user.py, category.py, sub_category.py, product.py,
            image_product.py, review.py, cart.py, cart_item.py, favorite.py)

9. authorization -> jwt(register, login, logout, generate_access_token)
10. admin -> sqladmin
11. FastAPI(wildberies) -> Server(AWS)









