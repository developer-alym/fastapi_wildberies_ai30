from .database import  Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (String, Integer, SmallInteger, Enum, ForeignKey,
                        Text, Boolean, Date, DateTime, Time)
from enum import Enum as PyEnum
from typing import Optional, List
from datetime import date, datetime


class StatusUser(str, PyEnum):
    gold = 'gold'
    silver = 'silver'
    bronze = 'bronze'
    simple = 'simple'

class UserProfile(Base):
    __tablename__ = 'user_profile'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    username: Mapped[str] = mapped_column(String(32), unique=True)
    email: Mapped[str] = mapped_column(String(32), unique=True)
    age: Mapped[int | None] = mapped_column(SmallInteger, default=0, nullable=True)
    phone_number: Mapped[str] = mapped_column(String, default='+996')
    profile_image: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[StatusUser] = mapped_column(Enum(StatusUser), default=StatusUser.simple)
    password: Mapped[str] = mapped_column(String)
    date_register: Mapped[date] = mapped_column(Date, default=date.today())

    product_owner: Mapped[List['Product']] = relationship('Product', back_populates='owner',
                                                          cascade='all, delete-orphan')
    user_review: Mapped[List['Review']] = relationship('Review', back_populates='user',
                                                       cascade='all, delete-orphan')
    cart_user: Mapped['Cart'] = relationship('Cart', back_populates='user',
                                             cascade='all, delete-orphan')
    favorite_user: Mapped[List['Favorite']] = relationship('Favorite', back_populates='user',
                                                     cascade='all, delete-orphan')
    refresh_owner: Mapped[List['RefreshToken']] = relationship('RefreshToken', back_populates='user',
                                                               cascade='all, delete-orphan')


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    token: Mapped[str] = mapped_column(String)

    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='refresh_owner')


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    category_name: Mapped[str] = mapped_column(String(32), unique=True)
    category_image: Mapped[str] = mapped_column(String)

    sub_category: Mapped[List['SubCategory']] = relationship('SubCategory',
                                                             back_populates='category', cascade='all, delete-orphan')
    category_product:  Mapped[List['Product']] = relationship('Product',
                                                              back_populates='category', cascade='all, delete-orphan')

    def __repr__(self):
        return self.category_name



class SubCategory(Base):
    __tablename__ = 'sub_category'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    sub_category_name: Mapped[str] = mapped_column(String(32))

    category: Mapped['Category'] = relationship('Category', back_populates='sub_category')
    sub_category_product: Mapped[List['Product']] = relationship('Product', back_populates='sub_category',
                                                                 cascade='all, delete-orphan')
    
    def __str__(self):
        return self.sub_category_name





class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    sub_category_id: Mapped[int] = mapped_column(ForeignKey('sub_category.id'))
    product_name: Mapped[str] = mapped_column(String(32))
    product_image: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column(SmallInteger, default=0)
    owner_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    category: Mapped['Category'] = relationship('Category', back_populates='category_product')
    sub_category: Mapped['SubCategory'] = relationship('SubCategory', back_populates='sub_category_product')
    owner: Mapped['UserProfile'] = relationship('UserProfile', back_populates='product_owner')
    images_product: Mapped[List['ImageProduct']] = relationship('ImageProduct', back_populates='product',
                                                                cascade='all, delete-orphan')
    review_product: Mapped[List['Review']] = relationship('Review', back_populates='product',
                                                          cascade='all, delete-orphan')
    item_product: Mapped[List['CartItem']] = relationship('CartItem', back_populates='product',
                                                    cascade='all, delete-orphan')
    favorite_product: Mapped[List['Favorite']] = relationship('Favorite', back_populates='product',
                                                              cascade='all, delete-orphan')

class ImageProduct(Base):
    __tablename__ = 'image_product'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    image: Mapped[str] = mapped_column(String)

    product: Mapped['Product'] = relationship('Product', back_populates='images_product')


class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    stars: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    video: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())

    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='user_review')
    product: Mapped['Product'] = relationship('Product', back_populates='review_product')


class Cart(Base):
    __tablename__ = 'cart'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'), unique=True)

    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='cart_user')
    items: Mapped[List['CartItem']] = relationship('CartItem', back_populates='cart',
                                                   cascade='all, delete-orphan')



class CartItem(Base):
    __tablename__ = 'cart_item'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    quantity: Mapped[int] = mapped_column(SmallInteger, default=1)

    cart: Mapped['Cart'] = relationship('Cart', back_populates='items')
    product: Mapped['Product'] = relationship('Product', back_populates='item_product')


class Favorite(Base):
    __tablename__ = 'favorite'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    like: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='favorite_user')
    product: Mapped['Product'] = relationship('Product', back_populates='favorite_product')




