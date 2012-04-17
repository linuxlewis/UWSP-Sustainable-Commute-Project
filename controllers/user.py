# USER API #

def login():
    return response.json({'user': { 'id': 111 } })

def get_id():
    return response.json({'user': { 'id':111, 'email':'example@email.com', 'uwspid':'exam111'} })

def location_create():
    return response.json({'result': "success" })

def create():
    return response.json({'user': { 'id':112, 'email':'example2@email.com', 'uwspid':'exam112'} })

