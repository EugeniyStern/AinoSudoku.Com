import sqlalchemy as db

engine = db.create_engine("mysql+mysqlconnector://eshern:PushMBR1!$@mysql.eshern.myjino.ru:3306/eshern")

conn = engine.connect()
result = conn.execute('select * from gantt_projects')
for _r in result:
    print( _r )