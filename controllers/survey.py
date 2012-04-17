def index(): 
    #clear userid if multiple users per machine
    if session.userid:
        del session.userid
 
    #uwsp form
    form=FORM(DIV(H3('UWSP ID:',_class='hlabel'),
    INPUT(_name='uwspid',_class='styledinput surveyinput',requires=IS_NOT_EMPTY()),_class='surveyrow'),
    DIV(LABEL('Department or office affiliation:',_class='hlabel',_for='uwdept'),
        SELECT(' ','Aber Suzuki Center','Academic Affairs','Accounting','Administration','Alumni Affairs','Anthropology','Athletics','Art and Design','Astronomy and Physics','Biology','Business and Economics','Chemistry','Continuing Education','Communication','Communicative Disorders','Computing & New Media Technologies','Computer Information Systems','Dance and Theatre','Education','English','Fisheries and Water Resources','Foreign Languages','Forestry','Geography and Geology','Health, Exercise Science and Athletics','Health Care Professions','Health Promotion & Human Development','Health Sciences','History','Human Dimensions of Natural Resources', 'Interior Architecture','Information Technology','Library','Maintenance','Mathematical Sciences','Military Science (R.O.T.C.)','Music','Paper Science and Engineering','Personnel Services','Philsophy','Physics and Astronomy','Physical Education & Athletic Training','Political Science','Psychology','Religious Studies','Reserve Officers Training Corps','Resource Management','Schmeeckle Reserve','Sociology & Social Work','Soil and Waste Resources','Student Affairs','Student Services','Theatre and Dance','University Relations','Water Resources','Web and Digital Media Development','Wildlife','Wildlife Ecology','Womens Studies',_name='uwdept',_class='surveyinput',_id='uwdept',requires=IS_NOT_EMPTY('select a value')),_class='surveyrow'),
    DIV(LABEL('UWSP Status:',_class='hlabel',_for='uwstatus'),SELECT(' ','Undergraduate','Graduate','Continuing Education','Faculty','Staff','Administration',_name='uwstatus',_value='Student',_class='surveyinput',_id='uwstatus',requires=IS_NOT_EMPTY('select a value')),_class='surveyrow'),
    DIV(LABEL('Years at UWSP:',_class='hlabel',_for='uwyears'),INPUT(_name='uwyears',_class='styledinput surveyinput',_id='uwyears',requires=IS_NOT_EMPTY()),_class='surveyrow'),
    DIV(INPUT(_type='submit',_value='start',_class='surveyinput',requires=IS_NOT_EMPTY()),_class='surveyrow'),_formname='form1')
    
    
    #if uwsp form validates
    if form.accepts(request,session,formname='form1'):
        session.uwspid = form.vars.uwspid
        session.uwstatus = form.vars.uwstatus
        session.uwyears = form.vars.uwyears
        session.uwdept = form.vars.uwdept
        session.isUwspUser = 1
        redirect(URL('address'))
    elif form.errors:
        response.flash = 'Please answer all questions' 
    return dict(form=form)

def address():

    #create address form
    form=FORM(
    DIV(
    DIV(H3('Live in the residence halls?',_class='hlabel'),INPUT(_name='dorm',_type='checkbox',_onclick='dormClick();',_id='dorm-check'),_class='surveyrow surveyhighlight'),
    DIV(H3('Local Address:',_class='hlabel'),INPUT(_name='addr',_class='styledinput surveyinput',requires=IS_NOT_EMPTY(),_id='addr'),_class='surveyrow'),
    DIV(H3('City:',_class='hlabel'),INPUT(_name='city',_class='styledinput surveyinput',requires=IS_NOT_EMPTY(),_id='city'),_class='surveyrow'),
    DIV(H3('State:',_class='hlabel'),INPUT(_name='state',_class='styledinput surveyinput',requires=IS_NOT_EMPTY(),_id='state'),_class='surveyrow'),
    DIV(H3('Zip Code:',_class='hlabel'),INPUT(_name='zip',_maxlength='5',_class='styledinput surveyinput',requires= [IS_NOT_EMPTY(),IS_MATCH('^\d{5}$',error_message='5 digit zip code')],_id='zip'),_class='surveyrow'),_class='top_address_form'),
    
    DIV(H3('Residence Hall:',_class='hlabel'),SELECT('','Neale','Baldwin','Steiner','Burroughs','Watson','Smith','May-Roach','Hansen','Knutzen','Hyer','Pray-Sims','Thomson','Suites@201',_class='surveyinput',_id='dorm-select'),_class='surveyrow hidden-div',_id='dorm_form'),
        DIV(INPUT(_type='button',_value='next',_class='surveyinput',_onclick='form_submit()'),_class='surveyrow'),
    _formname='address_form',_id='address-form')
    
    #initilize form2
    form2 = FORM()

    #query for result
    if session.uwspid:
        emailQuery = session.uwspid +'@uwsp.edu'
        result = db(db.response_user.email == emailQuery).select().first()
        #if uwsp user in our response data
        if result:
            #populate form
            response.flash = 'UWSP ID: ' + session.uwspid + ' found!'
            form.vars.addr = result.address
            form.vars.city = result.city
            form.vars.state = result.state
            form.vars.zip = result.zip
            session.fname = result.first_name
            session.lname = result.last_name
            session.email = result.email
            session.userid = result.id
        else:
            #query raw data
            result = db(db.user_data_raw.email==emailQuery).select() 
            #if user in raw data
            if(len(result) > 0):
                #populate form
                response.flash = 'UWSP ID: ' + session.uwspid + ' found!'
                form.vars.addr = result[0].ladd
                form.vars.city = result[0].lcity
                form.vars.state = result[0].lstate
                form.vars.zip = result[0].lzip.split(".")[0]  
                #save their name
                session.fname = result[0].first_
                session.lname = result[0].last_
                session.email = result[0].email   
            else:
                #uwsp user not in data
                #add additional information form
                response.flash = 'UWSP ID: ' + session.uwspid + ' not found! Fill out additional name information.'
                form2 = DIV(
                DIV(H3('First Name:',_class='hlabel'),INPUT(_name='fname',_class='styledinput surveyinput'),_class='surveyrow'),
                DIV(H3('Last Name:',_class='hlabel'),INPUT(_name='lname',_class='styledinput surveyinput'),_class='surveyrow'),
                DIV(H3('Email:',_class='hlabel'),INPUT(_name='email',_class='styledinput surveyinput',requires= [ IS_EMAIL(), IS_MATCH('^\w*@uwsp.edu$', error_message='Must be UWSP email')]),_class='surveyrow'))
                session.isUwspUser = 0
                form.insert(0,form2)
            
    #if address form validates
    if form.accepts(request,session,formname='address_form'):
        session.addr = form.vars.addr
        session.city = form.vars.city
        session.state = form.vars.state
        session.zip = form.vars.zip

        #if additional form was added
        if (form.vars.email != None):
            if (form.vars.fname != None): 
                session.fname = form.vars.fname
            if (form.vars.lname != None):
                session.lname = form.vars.lname
            session.email = form.vars.email
        
        #if response user exists
        if session.userid != None:
            #update
            result = db(db.response_user.id == session.userid).select().first()
            result.address = session.addr
            result.city = session.city
            result.zip = session.zip
            result.first_name = session.fname
            result.last_name = session.lname
            result.state = session.state
            result.update_record()
                    
        else:
            #insert new record
            session.userid = db.response_user.insert(address = session.addr, city = session.city,
                zip = session.zip, first_name = session.fname, last_name = session.lname, email = session.email,state=session.state)
            db.commit()

        #if user entered uwspid
        if session.uwspid:
            result = db(db.response_user.email == session.email).select().first()
            #TODO change logic for API calls
            uwspresult = db(db.uwsp_user.user == result.id).select().first()
            #if uwsp user already exists
            if uwspresult:
                #update record
                uwspresult.uwsp_id = session.uwspid
                uwspresult.uwsp_status = session.uwstatus
                uwspresult.uwsp_years = session.uwyears
                uwspresult.uwsp_dept = session.uwdept
                uwspresult.update_record()
            else:
                #insert new record
                db.uwsp_user.insert(uwsp_id = session.uwspid,uwsp_status = session.uwstatus, uwsp_years = session.uwyears,uwsp_dept = session.uwdept, user = result.id)        
        
        redirect(URL('modes'))
     
    return dict(form=form,form2=form2)

def modes():
    form = FORM(
    H2("How many days a week do you use each of these methods for your campus commute?",_class='highlight'),
    DIV(H3('Bike:',_class='hlabel float-left'),
    DIV(_class='tran_slider',_id='bike_slider'),
    INPUT(_type='text',_name='bike',_id='bike',_class='day-input'),H3('days',_class='hlabel'),_class='surveyrow'),
    DIV(H3('Bus:',_class='hlabel float-left'),
    DIV(_class='tran_slider',_id='bus_slider'),
    INPUT(_type='text',_name='bus',_id='bus',_class='day-input'),H3('days',_class='hlabel'),_class='surveyrow'),
    DIV(H3('Car:',_class='hlabel float-left'),
    DIV(_class='tran_slider', _id='car_slider'),
    INPUT(_type='text',_name='car',_id='car',_class='day-input'),H3('days',_class='hlabel'),_class='surveyrow'),
    DIV(H3('Carpool:',_class='hlabel float-left'),
    DIV(_class='tran_slider', _id='carpool_slider'),
    INPUT(_type='text',_name='carpool',_id='carpool',_class='day-input'),H3('days',_class='hlabel'),_class='surveyrow'),
    DIV(H3('Walk:',_class='hlabel float-left'),
    DIV(_class='tran_slider', _id='walk_slider'),
    INPUT(_type='text',_name='walk',_id='walk',_class='day-input'),H3('days',_class='hlabel'),_class='surveyrow'),
    DIV(H3('Telecommute:',_class='hlabel float-left'),
    DIV(_class='tran_slider', _id='telecommute_slider'),
    INPUT(_type='text',_name='telecommute',_id='telecommute',_class='day-input'),_class='surveyrow'))
    
    general_category = db(db.category.category_name=='route').select().first()
    general_question = db((db.question.category==general_category.id) & (db.question.type_id != 0)).select()
    general_container = DIV(H2("When are you on campus?",_class='highlight'),_id=general_category.category_name)

    question_id_list = []

    #general questions
    for question in general_question:
        element = getQuestion(question) 
        general_container.append(element)
        question_id_list.append(question.id)
    form.append(general_container)
    form.append(DIV(INPUT(_type='submit',_name='next',_value='next',_class='surveyinput'),_class='surveyrow'))

    if form.accepts(request):
        session.bike = form.vars.bike
        session.car = form.vars.car
        session.walk = form.vars.walk
        session.bus = form.vars.bus
        session.carpool = form.vars.carpool
        session.telecommute = form.vars.telecommute
        
        #insert varibles into database
        question = db(db.question.question_text == 'bike-days').select().first()
        db.response.update_or_insert(response_to=question.id,user=session.userid,answer=session.bike)
        
        question = db(db.question.question_text == 'car-days').select().first()
        db.response.update_or_insert(response_to=question.id,user=session.userid,answer=session.car)

        question = db(db.question.question_text == 'walk-days').select().first()
        db.response.update_or_insert(response_to=question.id,user=session.userid,answer=session.walk)

        question = db(db.question.question_text == 'bus-days').select().first()
        db.response.update_or_insert(response_to=question.id,user=session.userid,answer=session.bus)

        question = db(db.question.question_text == 'carpool-days').select().first()
        db.response.update_or_insert(response_to=question.id,user=session.userid,answer=session.carpool)

        question = db(db.question.question_text == 'telecommute-days').select().first()
        db.response.update_or_insert(response_to=question.id,user=session.userid,answer=session.telecommute)

        #general questions
        for question_id in question_id_list:
            answer_var = form.vars[str(question_id)]
            db.response.update_or_insert(response_to=question_id,user=session.userid,answer=answer_var)
        redirect('route')
    elif form.errors:
        response.flash = 'Please answer all questions'

    return dict(form=form,question_id_list=question_id_list)
   
def route():
#route based on session data
#query for user route
#return route path
    #if user is a uwspuser
    #if session.isUwspUser == 1:
        #set url for KML
    #    static_route = 'kml/2010/' + session.uwspid +'.kmz'
    #    kml_route = URL('static',static_route)
    #    session.viewRoute = 1
    #    session.setRoute = 0
    #else:
        #set varibles for generated route
    kml_route = '1'
    session.viewRoute = 0
    session.setRoute = 1

    #create confirmation form
    #form = FORM(
    #H2('Is this your route to UWSP?', _class='highlight'),
    #INPUT(_type='submit',_value='Yes',_name='map_accurate',_class='styledinput'),
    #INPUT(_type='submit',_value='No',_name='map_accurate',_class='styledinput'))
    
    #if confirmation form validates
    #if form.accepts(request):
        #if the user confirmmed the route
        #if request.vars.map_accurate == 'Yes':
            #delete uneeded session vars
        #    del session.setRoute
        #    del session.viewRoute
            #insert route into response table
        #    question = db(db.question.question_text == 'route to uwsp').select().first()
        #    response_user = db(db.response_user.email == session.email).select().first()
        #    db.response.update_or_insert(response_to=question.id,user=response_user.id,answer='true')
    
        # if session.walk != '0':
            #    redirect('walk')
         #   elif session.bike != '0':
            #    redirect('bike')
          #  elif session.car != '0':
            #    redirect('car')
           # elif session.bus != '0':
            #    redirect('bus')
            #elif session.carpool != '0':
             #   redirect('carpool')

        #else:
            #set session vars to create new route
    response.flash = 'Please edit and confirm your route'
        #    del session.viewRoute
        #    session.setRoute = 1

    #create drag route form
    form2 = FORM(
           H2('Please drag the route to reflect the route you take to UWSP', _class='highlight'),
           INPUT(_type='submit',_value='Confirm',_name='map_confirm',_class='styledinput '),
           INPUT(_type='button',_value='Reset',_class='styledinput',_onclick='clear_route(event);'),
           INPUT(_type='hidden',_name='route',_id='route', requires=IS_NOT_EMPTY()))
       
    #if the user confirmed their 'new' route
    if form2.accepts(request,session):
        if form2.vars.map_confirm == 'Confirm':
            #delete unneeded session vars
            del session.setRoute
            #insert new route into response table
            question = db(db.question.question_text == 'route to uwsp').select().first()
            response_user = db(db.response_user.email == session.email).select().first()
            db.response.update_or_insert(response_to=question.id,user=response_user.id,answer=form2.vars.route)

            if session.walk != '0':
                redirect('walk')
            elif session.bike != '0':
                redirect('bike')
            elif session.car != '0':
                redirect('car')
            elif session.bus != '0':
                redirect('bus')
            elif session.carpool != '0':
                redirect('carpool')
 
    return dict(kmlroute=kml_route,form2=form2)

def walk():
    #space for walk questions
    form = FORM(_id='work-form')

    walk_category = db(db.category.category_name=='walk').select().first()
    walk_question =  db((db.question.category==walk_category.id) & (db.question.type_id != 0)).select()
    walk_container = DIV(_id=walk_category.category_name)

    form.append(H2("Please evaluate your walking experience.",_class='highlight'))

    question_id_list = []

    #add each question from the database to the form
    for question in walk_question:
        element = getQuestion(question)
        walk_container.append(element)
        question_id_list.append(question.id)
    form.append(walk_container)
    form.append(DIV(INPUT(_type='submit',_value='next', _class='surveyinput'),_class='surveyrow'))

    #if form validates
    if form.accepts(request):
        for question in question_id_list:
            answer_var = form.vars[str(question)]
            db.response.update_or_insert(response_to=question,user=session.userid,answer=answer_var)
        redirect('walking')
    elif form.errors:
        response.flash = 'Please answer all questions.'

    return dict(form=form,question_id_list=question_id_list)

def walking():
    #space for walking map
    form = FORM(_id="walking-form")
    form.append(INPUT(_type='hidden',_name='walk',_id='walk-spots'))
    form.append(DIV(INPUT(_type='button',_name='next',_value='next',_class='surveyinput',_onclick='submitBikeMarker()'),_class='surveyrow'))

    if form.accepts(request):
        #save information
        question = db(db.question.question_text == 'walk-spots').select().first()
        db.response.update_or_insert(response_to = question.id, user=session.userid, answer=form.vars.walk)

        if session.bike != '0':
            redirect('bike')
        elif session.car != '0':
            redirect('car')
        elif session.bus != '0':
            redirect('bus')
        elif session.carpool != '0':
            redirect('carpool')
        else:
            redirect('final')

    elif form.errors:
        response.flash = 'error'

    return dict(form=form)

def bike():
    #space for biking questions
    form = FORM(_id='bike-form')
    bike_category = db(db.category.category_name=='bike').select().first()
    bike_question = db((db.question.category==bike_category.id) & (db.question.type_id != 0)).select()
    bike_container = DIV(_id=bike_category.category_name)

    form.append(H2("Please evaluate your biking experience.",_class='highlight'))

    question_id_list = []
    
    for question in bike_question:
        element = getQuestion(question)
        bike_container.append(element)
        question_id_list.append(question.id)
    form.append(bike_container)
    form.append(DIV(INPUT(_type='submit',_class='surveyinput', _value='next'),_class='surveyrow'))

    if form.accepts(request):
        for question in question_id_list:
            answer_var = form.vars[str(question)]
            db.response.update_or_insert(response_to=question,user=session.userid,answer=answer_var)
        redirect('biking')
    elif form.errors:
        response.flash = 'Please answer all questions.'
        
    return dict(question_id_list=question_id_list,form=form)

def biking():
    biking_form = FORM(
        INPUT(_type='submit',_value='next',_class='surveyinput',_onclick='submitBikeMarker()'),
        INPUT(_type='hidden',_name='bikes',_id='bike-rack-hidden',requires=IS_NOT_EMPTY(error_message='Please select atleast one bike rack location'))
        ,_id='bike-form')

    if biking_form.accepts(request):
        biking_rack = biking_form.vars.bikes
        question = db(db.question.question_text == 'bike-racks').select().first()
        response_user = db(db.response_user.email == session.email).select().first()
        db.response.update_or_insert(response_to=question.id,user=response_user.id,answer=biking_rack)

        #routing
        if session.car != '0':
            redirect('car')
        elif session.bus != '0':
            redirect('bus')
        elif session.carpool != '0':
            redirect('carpool')
        else:
            redirect('final')


    elif biking_form.errors:
        response.flash = 'Please select atleast one bike rack location'


    return dict(biking_form=biking_form)

def car():
    form = FORM()

    car_category = db(db.category.category_name=='car').select().first()
    car_question = (db((db.question.category==car_category.id) & (db.question.type_id != 0)).select()).sort(lambda row:row.question_order)

    car_container = DIV(_id=car_category.category_name)

    form.append(H2("Please evaluate your driving experience.",_class='highlight'))

    question_id_list = []

    for question in car_question:
        element = getQuestion(question)
        car_container.append(element)
        question_id_list.append(question.id)
    
    form.append(car_container)
    form.append(DIV(INPUT(_type='submit',_class='surveyinput', _value='next'),_class='surveyrow'))

    if form.accepts(request):
        for question in question_id_list:
            answer_var = form.vars[str(question)]
            db.response.update_or_insert(response_to=question,user=session.userid,answer=answer_var)
        redirect('parking')
    elif form.errors:
        response.flash = 'Please answer all questions.'

    return dict(form=form,question_id_list=question_id_list)

def parking():
    parking_lots_path = URL('static', 'kml/lots_outline.kmz')
    offcampus_path = URL('static', 'kml/off_campus_outline2.kmz')

    #parking lot form
    parking_form = FORM(
        INPUT(_type='submit',_value='next',_class='surveyinput',_onclick='submitLot()'),
        INPUT(_type='hidden',_name='campus_lots',_id='campus-hidden',requires=IS_NOT_EMPTY(error_message='Please select atleast one parking lot')),
        INPUT(_type='hidden',_name='off_lots',_id='off-hidden')
        ,_id='parking_form')

    if parking_form.accepts(request):
        parking_campus = parking_form.vars.campus_lots
        parking_off = parking_form.vars.off_lots

        #insert new parking lot response
        question = db(db.question.question_text == 'parking-lots-campus').select().first()
        db.response.update_or_insert(response_to=question.id,user=session.userid,answer=parking_campus)
        question = db(db.question.question_text == 'parking-lots-off').select().first()
        db.response.update_or_insert(response_to=question.id,user=session.userid,answer=parking_off)

        if session.bus != '0':
            redirect('bus')
        elif session.carpool != '0':
            redirect('carpool')
        else:
            redirect('final')

    elif parking_form.errors:
        response.flash = 'Please select atleast one parking location'

    return dict(parking_form=parking_form, parking_lots_path=parking_lots_path,offcampus_path=offcampus_path)


def bus():
    #bus questions
    form = FORM()
    bus_category = db(db.category.category_name=='bus').select().first()
    bus_question = db((db.question.category==bus_category.id) & (db.question.type_id != 0)).select()
    bus_container = DIV(_id=bus_category.category_name)

    form.append(H2('Please evaluate your bus experience',_class='highlight'))

    question_id_list = []
    
    for question in bus_question:
        element = getQuestion(question)
        bus_container.append(element)
        question_id_list.append(question.id)
    form.append(bus_container)
    form.append(DIV(INPUT(_type='submit',_class='surveyinput', _value='next'),_class='surveyrow'))

    if form.accepts(request):
        for question in question_id_list:
            answer_var = form.vars[str(question)]
            db.response.update_or_insert(response_to=question,user=session.userid,answer=answer_var)

            if session.carpool != '0': 
                redirect('carpool')
            else:
                redirect('final')

    elif form.errors:
        response.flash = 'Please answer all questions.'
        
    return dict(question_id_list=question_id_list,form=form)

def carpool():
    #carpool questions
    #bus questions
    form = FORM()
    carpool_category = db(db.category.category_name=='carpool').select().first()
    carpool_question = db((db.question.category==carpool_category.id) & (db.question.type_id != 0)).select()
    carpool_container = DIV(_id=carpool_category.category_name)

    question_id_list = []

    form.append(H2('Please evaluate your carpool experience',_class='highlight'))
    
    for question in carpool_question:
        element = getQuestion(question)
        carpool_container.append(element)
        question_id_list.append(question.id)
    form.append(carpool_container)
    form.append(DIV(INPUT(_type='submit',_class='surveyinput', _value='next'),_class='surveyrow'))

    if form.accepts(request):
        for question in question_id_list:
            answer_var = form.vars[str(question)]
            db.response.update_or_insert(response_to=question,user=session.userid,answer=answer_var)
            #routing
            redirect('carpool_parking')
                
    elif form.errors:
        response.flash = 'Please answer all questions.'
        
    return dict(question_id_list=question_id_list,form=form)

def carpool_parking():
    parking_lots_path = URL('static', 'kml/lots_outline.kmz')
    offcampus_path = URL('static', 'kml/off_campus_outline2.kmz')

    #parking lot form
    parking_form = FORM(
        INPUT(_type='submit',_value='next',_class='surveyinput',_onclick='submitLot()'),
        INPUT(_type='hidden',_name='campus_lots',_id='campus-hidden',requires=IS_NOT_EMPTY(error_message='Please select atleast one parking lot')),
        INPUT(_type='hidden',_name='off_lots',_id='off-hidden')
        ,_id='parking_form')

    if parking_form.accepts(request):
        parking_campus = parking_form.vars.campus_lots
        parking_off = parking_form.vars.off_lots

        #insert new parking lot response
        question = db(db.question.question_text == 'carpool-parking-lots-campus').select().first()
        db.response.update_or_insert(response_to=question.id,user=session.userid,answer=parking_campus)
        question = db(db.question.question_text == 'carpool-parking-lots-off').select().first()
        db.response.update_or_insert(response_to=question.id,user=session.userid,answer=parking_off)

        redirect('final')

    elif parking_form.errors:
        response.flash = 'Please select atleast one parking location'

    return dict(parking_form=parking_form, parking_lots_path=parking_lots_path,offcampus_path=offcampus_path)
def telecommute():
    return dict()

def final():
    return dict()

#helper method that generates HTML based on question type
def getQuestion(question):
        element = ''
        if question.type_id == '1':
            element = DIV(H3(question.question_text, _class="hlabel float-left"),TEXTAREA(_type='text',_cols="80",_class='styledinput float-left', _name=question.id, requires=IS_NOT_EMPTY()),_class='surveyrow')
        elif question.type_id == '2':
            element = DIV(H3(question.question_text, _class='hlabel'),INPUT(_type='text',_class='surveyinput styledinput', _name=question.id,requires=IS_NOT_EMPTY()),_class='eightcol surveyrow')
        elif question.type_id == '3':
            element = DIV(H3(question.question_text, _class='float-left'),INPUT(_type='text',_class='styledinput timeinput highlight float-right', _name=question.id,
                requires=IS_NOT_EMPTY(),_id="time-input-"+str(question.id)),_class='surveyrow')
        elif question.type_id == '4':
            element = DIV(H3(question.question_text,_class='float-left'),DIV(_id="minute-slider-"+str(question.id),_class="minute-slider float-left"),INPUT(_type="text",_name=question.id,_id="slider-input-"+str(question.id),_class="minute-input"),H3('minutes',_class='float-left'),_class='tab-surveyrow')
        elif question.type_id == '5':
            element = DIV(H3(question.question_text,_class='float-left'),DIV(_id="hour-slider-"+str(question.id),_class="hour-slider float-left"),INPUT(_type="text",_name=question.id,_id="slider-input-"+str(question.id),_class="minute-input"),H3('hours',_class='float-left'),_class='tab-surveyrow') 
        elif question.type_id == '6':
            element = DIV(H3(question.question_text,_class='float-left'),_class='surveyrow')
            select = SELECT(_name=question.id,_id=question.id,_class="tabinput surveyinput float-left",requires=IS_NOT_EMPTY())
            select.append(" ")
            options = question.answers.split(',')
            for option in options:
                select.append(option)
            element.append(select) 
        elif question.type_id == '7':
            element = DIV(H3(question.question_text),DIV(_id="people-slider-"+str(question.id),_class="people-slider"),INPUT(_type="text",_name=question.id,_id="slider-input-"+str(question.id),_class="minute-input"),H3('people',_class='float-left'),_class='tab-surveyrow') 
        elif question.type_id == '8':
            element = DIV(H3(question.question_text),DIV(_id="week-slider-"+str(question.id),_class="week-slider"),INPUT(_type="text",_name=question.id,_id="slider-input-"+str(question.id),_class="minute-input"),H3('days',_class='float-left'),_class='tab-surveyrow') 
        elif question.type_id == '9':
            element = DIV(H3(question.question_text),DIV(_id="month-slider-"+str(question.id),_class="month-slider"),INPUT(_type="text",_name=question.id,_id="slider-input-"+str(question.id),_class="minute-input"),H3('days',_class='float-left'),_class='tab-surveyrow')  
        elif question.type_id == '10':
            element = DIV(H3(question.question_text, _class='float-left'),_class='tab-surveyrow')
            list_element = UL(_id=question.id, _class='check-list')
            for option in question.answers.split(','):
                list_element.append(LI(DIV(INPUT(_type='checkbox', _class='checkbox-'+str(question.id),_value=option),H4(option,_class='label')),_class='error-border'))
            element.append(list_element)
            element.append(INPUT(_type='hidden',_name=question.id,_id='check-list-hidden-'+str(question.id)))
        elif question.type_id == '11':
            element = DIV(H3(question.question_text),DIV(_id="year-slider-"+str(question.id),_class="year-slider"),INPUT(_type="text",_name=question.id,_id="slider-input-"+str(question.id),_class="minute-input"),H3('years',_class='float-left'),_class='tab-surveyrow')  
        return element

def survey_redirect():

    return 0


    



