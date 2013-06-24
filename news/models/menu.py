# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = 'Новости'

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Новости по категориям'), False, URL('default', 'index'), []),
    (T('Все новости'), False, URL('default', 'show_all'), [])
]

DEVELOPMENT_MENU = True

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    # useful links to internal and external resources
    if auth.is_logged_in():
        response.menu += [
            (SPAN('Администрирование', _class='highlighted'), False, '', [
            ('Добавить категорию', False, URL('category_add')),
            ('Добавить новость', False, URL('add')),
            ]
        )]
if DEVELOPMENT_MENU: _()

if "auth" in locals(): auth.wikimenu()