# -*- coding: utf-8 -*-

import datetime
from gluon.tools import *

"""
Строка подключения к БД
"""
db = DAL('oracle://test/test@xe')

"""
Создание таблиц для авторизации пользователей
"""
auth = Auth(db)
auth.define_tables()

"""
Таблица Категории
"""
db.define_table('category',
    Field('title', unique=True))

"""
Таблица Новости
"""
db.define_table('news',
   Field('id_category', db.category, ondelete='CASCADE'),
   Field('title', unique=True),
   Field('newsdate', 'date', default=request.now),
   Field('image', 'upload', autodelete=True),
   Field('anons', 'string', length=1024),
   Field('body', 'text'),
   Field('id_user', db.auth_user, default=auth.user_id, readable=False, writable=False),
   format = '%(title)s',
   fake_migrate=True)

"""
Валидация полей
"""
db.news.id_category.requires = IS_IN_DB(db, db.category.id, '%(title)s')
db.category.title.requires = IS_NOT_EMPTY()

db.news.title.requires = IS_NOT_EMPTY()
db.news.newsdate.requires = IS_DATE_IN_RANGE(format=T('%Y-%m-%d'),
                                             maximum=datetime.date.today(),
                                             error_message='Дата новости не может быть больше текущей!')
db.news.body.requires = IS_NOT_EMPTY()
db.news.anons.requires = IS_LENGTH(1024)
db.news.id_user.requires = IS_NOT_EMPTY()
db.news.image.requires = IS_IMAGE(extensions=('jpeg', 'png'), maxsize=(800, 600), minsize=(150, 100))
   
   
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
crud, service, plugins = Crud(db), Service(), PluginManager()

## настройка почты
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## настройка авторизации пользователей
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')
