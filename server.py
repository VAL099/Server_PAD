from fastapi import FastAPI, Response, Header, HTTPException

import mysql.connector as msql
import const, models, handlers, os

server = FastAPI()

db = msql.connect(host = 'host.docker.internal', port = os.getenv('db_port'), user = const.DB_USERNAME, password = const.DB_PASSWORD, database = 'll2_pad') # connect to db
cursor = db.cursor()

@server.get('/')
async def home():
    return {'message':'Welcome!'}

@server.get('/adv/all')
async def get_all(authorisation_token:str = Header()):
    if authorisation_token == const.AUTH_TOKEN:
        return_data = []
        cursor.execute(f'SELECT * FROM adverts')
        data = cursor.fetchall()
        if data != None:
            for advert in data:
                return_data.append( handlers.serialiser(advert[0],advert[1],advert[2],advert[3],advert[4]) )
            return return_data
        else: 
            raise HTTPException(status_code = 404, detail='Not found!')
    else: 
        raise HTTPException(status_code = 404, detail='Wrong Authentication!')

@server.get('/adv/category')
async def get_by_categories(c, authorisation_token:str = Header()):
    if authorisation_token == const.AUTH_TOKEN:
        return_data = []
        cursor.execute(f'SELECT * FROM adverts where category = %s',(c,))
        data = cursor.fetchall()
        if data != None:
            for advert in data:
                return_data.append( handlers.serialiser(advert[0],advert[1],advert[2],advert[3],advert[4]) )
            return return_data
        else: 
            raise HTTPException(status_code = 404, detail='Not found!')
    else: 
        raise HTTPException(status_code = 404, detail='Wrong Authentication!')

@server.get('/adv/categories')
async def get_all_categories(authorisation_token:str = Header()):
    if authorisation_token == const.AUTH_TOKEN:
        cursor.execute('SELECT category from adverts')
        data = cursor.fetchall()
        return set(data)
    else: 
        raise HTTPException(status_code = 404, detail='Wrong Authentication!')

@server.get('/adv/id')
async def get_by_id(adv_id, authorisation_token:str = Header()):
    if authorisation_token == const.AUTH_TOKEN:
        cursor.execute(f'SELECT * FROM adverts where id = {adv_id}')
        try:
            data = cursor.fetchall()[0]
            return handlers.serialiser( data[0],data[1],data[2],data[3],data[4] )
        except IndexError: 
            raise HTTPException(status_code = 404, detail='Not found!')
    else: 
        raise HTTPException(status_code = 404, detail='Wrong Authentication!')

@server.post('/adv/post')
async def post_advert(item: models.Advert, authorisation_token:str = Header()):
    if authorisation_token == const.AUTH_TOKEN:
        query = "INSERT INTO adverts (category, title, description, price) VALUES (%s, %s, %s, %s)"
        data = (item.category, item.title, item.description, item.price)
        cursor.execute(query, data); db.commit()
        return Response(status_code = 201)
    else: 
        raise HTTPException(status_code = 404, detail='Wrong Authentication!')

@server.patch('/adv/patch')
async def patch_advert(adv_id, item:dict, authorisation_token:str = Header()):
    if authorisation_token == const.AUTH_TOKEN:
        to_upd = ''; data = ()
        for key in list(item.keys()):
            to_upd += f'{key} = %s,'
            data += (item[key],)
        to_upd = to_upd.rstrip(',')
        query = f'UPDATE adverts SET {to_upd} WHERE id = {adv_id}'
        cursor.execute(query, data); db.commit()
        return Response(status_code = 202)
    else: 
        raise HTTPException(status_code = 404, detail='Wrong Authentication!')

@server.delete('/adv/rm')
async def remove_advert(adv_id, authorisation_token:str = Header()):
    if authorisation_token == const.AUTH_TOKEN:
        cursor.execute(f'DELETE FROM adverts where id = {adv_id}'); db.commit()
        return Response(status_code = 204)
    else: 
        raise HTTPException(status_code = 404, detail='Wrong Authentication!')
