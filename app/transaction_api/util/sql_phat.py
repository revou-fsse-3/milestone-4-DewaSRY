from os import environ


USER_NAME=environ.get('USER_NAME') 
PASSWORD=environ.get('PASSWORD')
DB_NAME=environ.get('DB_NAME')
SERVER=environ.get('SERVER')



my_sql=f"mysql+mysqlconnector://{USER_NAME}:{PASSWORD}@{SERVER}/{DB_NAME}"


