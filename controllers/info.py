# coding: utf8
# try something like
def index(): return dict(message="hello from info.py")

def about():return dict()

def people():return dict()

def funding():
    links = {
        'Funding':{
            'Geographic Information System Center':'http://www.uwsp.edu/gis',
            'Wisconsin Institute Sustinable Technology':'http://www.uwsp.edu/wist/Pages/default.aspx'}
         }
    return links
def news():
    #query news article table
    #package results in dictionary
    return dict(article_list=db().select(db.articles.ALL))
@auth.requires_login()
def add_news():
    form = SQLFORM(db.articles)
    if form.process().accepted:
        response.flash = 'Article Added'
    elif form.errors:
        response.flash = 'Form Error'
    else:
        response.flash = 'Please fill out article form'
    return dict(form=form)
def delete_news():
    return dict()
@auth.requires_login()
def query():
    if(request.get_vars.q):
        result = db(db.user_data_raw.email==request.vars.q).select()
        return dict(result=result)
    else:
        return dict(result=dict())
def gallery():
    #query gallery table
    #for each gallery
        #select image rows
        #for each row
            #add dict(name,descrip,img)
         #add dict of image_nodes to gallery dict
    #return gallery
    return dict()
