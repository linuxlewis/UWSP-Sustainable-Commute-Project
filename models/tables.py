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
                Field('uwsp_years'))

db.define_table('category',
                Field('category_name'))
#initialize categories
db.category.update_or_insert(dict(category_name='route'),category_name='route')
db.category.update_or_insert(dict(category_name='address'),category_name='address')
db.category.update_or_insert(dict(category_name='bike'),category_name='bike')
db.category.update_or_insert(dict(category_name='car'),category_name='car')
db.category.update_or_insert(dict(category_name='bus'),category_name='bus')


db.define_table('question',
                Field('question_text'),
                Field('category',db.category))
                
db.define_table('response',
                Field('response_to',db.question),
                Field('user',db.response_user),
                Field('answer','text'))# coding: utf8
