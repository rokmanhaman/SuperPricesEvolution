from fastapi import FastAPI, HTTPException, Path
from pymongo import MongoClient
from pymongo import ASCENDING
from urllib.parse import quote_plus

from config import DB_NAME, DB_COLLECTION, DB_USER, DB_USER_PASS, DB_HOST, DB_PORT



app = FastAPI()

# Conexión a la base de datos MongoDB
escaped_user = quote_plus(DB_USER)
escaped_pass = quote_plus(DB_USER_PASS)

connection_url = f"mongodb://{escaped_user}:{escaped_pass}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

client = MongoClient(connection_url)
db = client[DB_NAME]
collection = db[DB_COLLECTION]

@app.get("/items/{item_id}")
async def read_item(item_id: str = Path(..., min_length=7, max_length=7, description="un id de ejemplo es 3390322")):
    # Buscar los items en la colección que coincidan con el ID
    items = collection.find({"prod_id": item_id}).sort("date", ASCENDING)
    
    # Crear una lista para almacenar los resultados
    result = []
    
    # Iterar sobre los resultados y agregarlos a la lista
    for item in items:
        # Convertir el ObjectId a una cadena antes de agregarlo a la lista
        item['_id'] = str(item['_id'])
        result.append(item)
    
    # Verificar si se encontraron elementos
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Item not found")