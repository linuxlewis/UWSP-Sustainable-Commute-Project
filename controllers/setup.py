#sets up the database with data
@auth.requires_login()
def setupdb():

    #initialize categories
    db.category.update_or_insert(category_name='route')
    db.category.update_or_insert(category_name='parking')
    db.category.update_or_insert(category_name='address')
    db.category.update_or_insert(category_name='bike')
    db.category.update_or_insert(category_name='car')
    db.category.update_or_insert(category_name='bus')
    db.category.update_or_insert(category_name='walk')
    db.category.update_or_insert(category_name='data')
    db.category.update_or_insert(category_name='carpool')
    db.category.update_or_insert(category_name='telecommute')

    #question types
#0 = data
#1 = text area answer
#2 = input answer
#3 = time answer, options in answers
#4 = slider answer, options in answers
#5 = slider hour,
#6 = select
#7 = people slider
#8 = week day slider
#9 = month day slider
#10 check all apply, options in answers
#11 = 20 year slider

#insert survey question into database

#school route
    category = db(db.category.category_name == 'data').select().first()
    db.question.update_or_insert(question_text='route to uwsp',category=category.id,type_id=0)

    category = db(db.category.category_name == 'route').select().first()

#initialize questions
###General questions about peoples' commute, regardless of mode
    #db.question.update_or_insert(question_text='How many hours a week do you spend on campus?',category=category.id,type_id=5)
            #0-10,10-20,20-30,30-40,40 and up.
    db.question.update_or_insert(question_text='When do you typically arrive on campus?',category=category.id,type_id=3)
            #Before 8am, 8-10,10-12,after 12
    db.question.update_or_insert(question_text='When do you leave campus?',category=category.id,type_id=3) 
            #Before 12, 12-2,2-4,4-6,after 6
    #db.question.update_or_insert(question_text='About how many minutes does it take to get from your front door to your first destination on campus?',category=category.id,type_id=4) 
            #Slider from 1 to 180 (three hours) or write in a number##

#parking locations
    category = db(db.category.category_name == 'parking').select().first()

#telecommute questions
    categoy = db(db.category.category_name == 'telecommute').select().first()
    db.question.update_or_insert(question_text='telecommute-days',category=category.id,type_id=0)

#transportation
    #bike questions
    category = db(db.category.category_name == 'bike').select().first()
    db.question.update_or_insert(question_text='bike-days',category=category.id,type_id=0)
    db.question.update_or_insert(question_text='bike-racks',category=category.id,type_id=0)
    db.question.update_or_insert(question_text='How long does it take you to bike to campus?', category=category.id, type_id=4)
    db.question.update_or_insert(question_text='How many days do you leave your bike on campus overnight?',category=category.id,type_id=8)
    db.question.update_or_insert(question_text='How many years have you been bicycle commuting to campus?', category=category.id, type_id=11)
    db.question.update_or_insert(question_text='What type of biker are you? (check all that apply)',category=category.id, type_id=10, answers='Hard core --- nothing stops me from biking,           Dedicated        ---   snows is a no go      , Waterproof -- there\'s nothing wrong with rain, Sunny -- my bike does\'t like getting wet, Unpredictable -- inspiration overcomes some obsticles')
    db.question.update_or_insert(question_text='bike-spots', category=category.id, type_id=0)

    #carpool questions
    category = db(db.category.category_name == 'carpool').select().first()
    db.question.update_or_insert(question_text='carpool-days',category=category.id,type_id=0)
    db.question.update_or_insert(question_text='carpool-parking-lots-campus', category=category.id, type_id=0)
    db.question.update_or_insert(question_text='carpool-parking-lots-off', category=category.id, type_id=0)
    db.question.update_or_insert(question_text='How long have you been commuting by carpool?', category=category.id, type_id=11)
    db.question.update_or_insert(question_text='What do you like about your car ride?', category=category.id, type_id=1)
    db.question.update_or_insert(question_text='How could your car commute be improved?', category=category.id, type_id=1)
    db.question.update_or_insert(question_text='How many people, driver and passengers are on board when you arrive?',category=category.id,type_id=7)




    #car questions
    category = db(db.category.category_name == 'car').select().first()
    db.question.update_or_insert(question_text='parking-lots-campus', category=category.id,type_id=0)
    db.question.update_or_insert(question_text='parking-lots-off', category=category.id,type_id=0)
    db.question.update_or_insert(question_text='car-days',category=category.id,type_id=0)

    db.question.update_or_insert(question_text='Make:',category=category.id,type_id=2, question_order=1)
    db.question.update_or_insert(question_text='Model:',category=category.id,type_id=2, question_order=2)
    db.question.update_or_insert(question_text='Plate:',category=category.id,type_id=2, question_order=3)
    db.question.update_or_insert(question_text='Year:', category=category.id,type_id=2, question_order=4)
#fuel type:
    db.question.update_or_insert(question_text='Fuel Type:',category=category.id,type_id=6,answers="gasoline, diesel, biodiesel, hybrid, electric", question_order=5)
    db.question.update_or_insert(question_text='Do you purchase a parking permit?', category=category.id, answers='Yes, No',type_id=6, question_order=6)

    db.question.update_or_insert(question_text='Do you use metered spaces?', category=category.id,answers='Yes, No, Sometimes',type_id=6, question_order=7)

    db.question.update_or_insert(question_text='How many people, driver and passengers are on board when you arrive?',category=category.id,type_id=7, question_order=8)
        
    #bus questions
    category = db(db.category.category_name == 'bus').select().first()
    db.question.update_or_insert(question_text='bus-days',category=category.id,type_id=0)
    db.question.update_or_insert(question_text='How long have you commuted by bus?', category=category.id, type_id=11)
    db.question.update_or_insert(question_text='How many minutes do you walk to the bus stop?', category=category.id, type_id=4)
    db.question.update_or_insert(question_text='What do you like about your bus ride?', category=category.id, type_id=1)
    db.question.update_or_insert(question_text='How could your bus commute be improved?', category=category.id, type_id=1)


    #walking questions
    category = db(db.category.category_name == 'walk').select().first()
    db.question.update_or_insert(question_text='walk-days',category=category.id,type_id=0)
    db.question.update_or_insert(question_text='How long does it take you to walk to campus?', category=category.id, type_id=4)
    db.question.update_or_insert(question_text='Which weather conditions are not suitable for commuting on foot? Check all that apply.',type_id=10, category=category.id, answers='Sunny,Temperature,Overcast,Raining,Wet streets,Snowing,Snow on streets, Night time')
    db.question.update_or_insert(question_text='What changes would improve your walk experience?', category=category.id, type_id=1)
    db.question.update_or_insert(question_text='walk-spots',category=category.id,type_id=0)


    return dict(status='success')
