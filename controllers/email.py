# coding: utf8
# try something like
def index():
     db.email_list.insert(emailID=request.vars.T1)
     redirect('http://www.uwsp.edu/wist/Pages/research/commuteProject.aspx')
     return dict()
def local():
    db.email_list.insert(emailID=request.vars.T1)
    session.flash=T(request.vars.T1 + " added to subscriber list!")
    redirect(URL('default','index'))
    return dict()
