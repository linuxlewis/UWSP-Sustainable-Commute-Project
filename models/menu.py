# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################


response.subtitle = T('UWSP Sustainable Commute Project')
response.title = response.subtitle
#http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Sam Bolgert'
response.meta.description = 'Free and open source full-stack enterprise framework for agile development of fast, scalable, secure and portable database-driven web-based applications. Written and programmable in Python'
response.meta.keywords = 'uwsp, commute, sustainability'
response.meta.generator = 'UWSP Sustainable Commute'
response.meta.copyright = 'Copyright 2011'


##########################################
## this is the main application menu
## add/remove items as required
##########################################

response.menu = [
    (T('HOME'), False, URL('default','index'), []),
    (T('ABOUT v'), False,URL('default','index'),[
        (T('LATEST NEWS'),False,URL('info','news'),[]),
        (T('PEOPLE'),False,URL('info','people'),[]),
        (T('FUNDING'),False,URL('info','funding'),[])]),
    (T("PROJECT OUTCOMES v"),False,URL('default','index'),[
        (T('GRAPHS AND CHARTS'),False,URL('info','gallery'),[])]),        
    (T("COMMUTING SURVEY"),False,URL('survey','index'),[]),
    (T("BUS OPTIONS"),False,URL('map_widget','index'),[])
    ]

##########################################
## this is here to provide shortcuts
## during development. remove in production
##
## mind that plugins may also affect menu
##########################################

#########################################
## Make your own menus
##########################################

#response.menu+=[
 #   (T('This App'), False, URL('admin', 'default', 'design/%s' % request.application),
   #  [
  #          (T('Controller'), False,
   #          URL('admin', 'default', 'edit/%s/controllers/%s.py' \
    #                 % (request.application,request.controller=='appadmin' and
      #                  'default' or request.controller))),
     #       (T('View'), False,
      #       URL('admin', 'default', 'edit/%s/views/%s' \
  #                   % (request.application,response.view))),
    #        (T('Layout'), False,
   #          URL('admin', 'default', 'edit/%s/views/layout.html' \
    #                 % request.application)),
   #         (T('Stylesheet'), False,
     #        URL('admin', 'default', 'edit/%s/static/base.css' \
      #               % request.application)),
       #     (T('DB Model'), False,
#             URL('admin', 'default', 'edit/%s/models/db.py' \
 #                    % request.application)),
  #          (T('Menu Model'), False,
   #          URL('admin', 'default', 'edit/%s/models/menu.py' \
    #                 % request.application)),
     #       (T('Database'), False,
      #       URL(request.application, 'appadmin', 'index')),
#
    #        (T('Errors'), False,
     #        URL('admin', 'default', 'errors/%s' \
      #               % request.application)),

       #     (T('About'), False,
        #     URL('admin', 'default', 'about/%s' \
         #            % request.application)),

     #       ]
 #  )]


##########################################
## this is here to provide shortcuts to some resources
## during development. remove in production
##
## mind that plugins may also affect menu
##########################################
