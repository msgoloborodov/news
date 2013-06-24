# -*- coding: utf-8 -*-

def index():
    """
    Основной контроллер.
    Новости по категориям.
    """
    count = db.news.id.count()
    categories = db().select(db.category.ALL,count,
                           left=db.news.on(db.news.id_category==db.category.id),
                           groupby=(db.category.id,db.category.title),
                           orderby=db.category.title)
    
    news={}
    for row in categories:
        rows = None
        if row[count] > 3:
            rows = db(db.news.id_category==row.category.id).select(db.news.ALL, orderby='<random>', limitby=(0,3)).sort(lambda row: row.newsdate, reverse=True)
        else:
            rows = db(db.news.id_category==row.category.id).select(db.news.ALL, orderby=~db.news.newsdate)
        
        news.update({row.category.id: rows})
            
    return dict(news=news, categories=categories,count=count)
    
def show_all():
    """
    Все новости.
    """
    news = db().select(db.news.ALL,orderby=~db.news.newsdate)
    return dict(news=news)

def show():
    """
    Просмотр новости.
    """
    news = db.news(request.args(0)) or redirect(URL('index'))
    return dict(news=news)
    
@auth.requires_login()
def add():
    """
    Добавление новости. 
    """
    form = SQLFORM(db.news)
    if form.process().accepted:
        response.flash = 'Новость добавлена'
    elif form.errors:
       response.flash = 'Ошибки'
    return dict(form=form)

@auth.requires_login()
def edit():
    """
    Редактирование новости. 
    """
    record = db.news(request.args(0)) or redirect(URL('index'))
    form = SQLFORM(db.news, record, 
                   deletable = True,
                   upload=URL('download'))
    if form.process().accepted:
        response.flash = 'Новость сохранена'
    elif form.errors:
       response.flash = 'Ошибки'
    return dict(form=form)

@auth.requires_login()    
def category_add():
    """
    Добавление категории. 
    """
    form = SQLFORM(db.category)
    if form.process().accepted:
        response.flash = 'Категория добавлена'
    elif form.errors:
       response.flash = 'Ошибки'
    return dict(form=form)

@auth.requires_login()    
def category_edit():
    """
    Редактирование категории. 
    """
    record = db.category(request.args(0)) or redirect(URL('index'))
    form = SQLFORM(db.category, record, 
                   deletable = True)
    if form.process().accepted:
        response.flash = 'Категория сохранена'
    elif form.errors:
       response.flash = 'Ошибки'
    return dict(form=form)    

@cache.action()    
def download():
    """
    Контроллер отвечающи за скачивание загруженных файлов. 
    """
    return response.download(request, db)

def user():
    """
    Авторизации пользователя
    """
    return dict(form=auth())

def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
