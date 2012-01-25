import datetime
db.define_table('articles',
                    Field('author',db.auth_user),
                    Field('title','text'),                
                    Field('published','date',default=datetime.datetime.now()),
                    Field('bodytext','text'))
db.articles.author.requires = IS_IN_DB(db,'auth_user.id','auth_user.first_name')
db.articles.bodytext.requires = IS_NOT_EMPTY()
db.articles.title.requires = IS_NOT_EMPTY()

#define email table
db.define_table('email_list',Field('emailID','string'))

db.define_table('user_data_debug',
                    Field('first_name'),
                    Field('last_name'),
                    Field('email'),
                    Field('uwsp_id'),
                    Field('home_address'),
                    Field('home_city'),
                    Field('home_state'),
                    Field('home_zip'),
                    Field('home_phone'),
                    Field('local_address'),
                    Field('local_city'),
                    Field('local_state'),
                    Field('local_zip'),
                    Field('local_phone'))
                    
db.define_table('user_data_raw',
                    Field('first_'),
                    Field('last_'),
                    Field('email'),
                    Field('hadd'),
                    Field('hcity'),
                    Field('hstate'),
                    Field('hzip'),
                    Field('hphone'),
                    Field('ladd'),
                    Field('lcity'),
                    Field('lstate'),
                    Field('lzip'),
                    Field('lphone'),
                    Field('miles'))
db.define_table('response_user',
                    Field('first_name'),
                    Field('last_name'),
                    Field('email'),
                    Field('address'),
                    Field('city'),
                    Field('zip'),
                    Field('state'))
db.define_table('uwsp_user',
                Field('user',db.response_user),
                Field('uwsp_id'),
                Field('uwsp_status'),
                Field('uwsp_years'),
                Field('uwsp_dept'))

db.define_table('category',
                Field('category_name'))
#initialize categories
db.category.update_or_insert(category_name='route')
db.category.update_or_insert(category_name='parking')
db.category.update_or_insert(category_name='address')
db.category.update_or_insert(category_name='bike')
db.category.update_or_insert(category_name='car')
db.category.update_or_insert(category_name='bus')
db.category.update_or_insert(category_name='walk')
db.category.update_or_insert(category_name='data')

#inialize questions table
db.define_table('question',
                Field('question_text'),
                Field('category',db.category))

#insert survey question into database

#school route
category = db(db.category.category_name == 'data').select().first()
db.question.update_or_insert(question_text='route to uwsp',category=category.id)

category = db(db.category.category_name == 'route').select().first()

#initialize questions
###General questions about peoples' commute, regardless of mode
db.question.update_or_insert(question_text='How many hours a week do you spend on campus?',category=category.id)
        #0-10,10-20,20-30,30-40,40 and up.
db.question.update_or_insert(question_text='When do you typically arrive on campus?',category=category.id)
        #Before 8am, 8-10,10-12,after 12
db.question.update_or_insert(question_text='When do you leave campus?',category=category.id) 
        #Before 12, 12-2,2-4,4-6,after 6
db.question.update_or_insert(question_text='About how many minutes does it take to get from your front door to your first destination on campus?',category=category.id) 
        #Slider from 1 to 180 (three hours) or write in a number##

#parking locations
category = db(db.category.category_name == 'parking').select().first()
db.question.update_or_insert(question_text='parking lots', category=category.id)

#transportation
category = db(db.category.category_name == 'bike').select().first()
db.question.update_or_insert(question_text='bike-days',category=category.id)

category = db(db.category.category_name == 'car').select().first()
db.question.update_or_insert(question_text='car-days',category=category.id)

category = db(db.category.category_name == 'bus').select().first()
db.question.update_or_insert(question_text='bus-days',category=category.id)

category = db(db.category.category_name == 'walk').select().first()
db.question.update_or_insert(question_text='walk-days',category=category.id)

#inialize response table
db.define_table('response',
                Field('response_to',db.question),
                Field('user',db.response_user),
                Field('answer','text'))
