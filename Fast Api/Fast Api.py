import io
from typing import Dict, Optional

from fastapi import FastAPI
from enum import Enum

from pydantic import BaseModel
from fastapi.responses import ORJSONResponse, UJSONResponse, HTMLResponse, StreamingResponse
import pandas as pd


app = FastAPI()

class RoleName(str, Enum):
    admin = 'Admin'
    writer = 'Writer'
    reader = 'Reader'

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.get("/")
def root():
    return {"messsage": "Hello World, from Galileo Master!!! Section V"}

@app.get("/itemss/{item_id}")
def read_item(item_id: int) -> Dict[str, int]:
    return {"item_id": item_id}


@app.get("/users/me")
def read_current_user():
    return {"user_id": "The current logged user."}


@app.get("/users/{user_id}")
def read_user(user_id: str):
    return {"user_id": user_id}


@app.get("/roles/{role_name}")
def get_role_permissions(role_name: RoleName):
    #return role permissions
    if role_name == RoleName.admin:
        return {"role_name": role_name, "permissions": "Full access"}

    if role_name == RoleName.writer:
        return {"role_name": role_name, "permissions": "Writer access"}
    
    return {"role_name": role_name, "Permissions": "Read access only"}


fake_items_db = [{"item_name": "uno"}, {"item_name": "dos"}, {"item_name": "tres"}]

@app.get("/items/")
def read_items(skip: int, limit: int):
    return fake_items_db[skip: skip + limit]


@app.get("/items/{item_id}")
def read_item_query(item_id: int, query: Optional[str] = None):
    message = {"item_id": item_id}
    if query:
        message['query'] = query

    return message


@app.get("/users/{user_id}/items/{item_id}")
def read_user_item(user_id: int, item_id: int, query: Optional[str] = None, describe: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}

    if query:
        item['query'] = query

    if describe:
        item['description'] = "This is a long description for the item"
    
    return item


@app.post("/items/")
def create_item(item: Item):
    return{
        "message": "The item was successfully created",
        "item": item.dict()
    }


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item.tax == 0 or item.tax is None:
        item.tax = item.price * 0.12

    return {
        "message": "The item was updated",
        "item_id": item_id,
        "item": item.dict()
    }


@app.get("/itemsall", response_class=UJSONResponse)
def read_long_json():
    return [{"item_id": "item"},{"item_id": "item"},{"item_id": "item"},{"item_id": "item"},
            {"item_id": "item"},{"item_id": "item"},{"item_id": "item"},{"item_id": "item"},
            {"item_id": "item"},{"item_id": "item"},{"item_id": "item"},{"item_id": "item"},
            {"item_id": "item"},{"item_id": "item"},{"item_id": "item"},{"item_id": "item"}]


@app.get("/html", response_class=HTMLResponse)
def read_html():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """



@app.get("/csv")
def get_csv():
    df = pd.DataFrame({"Column A": [1, 2], "Column B": [3, 4]})

    stream = IOBase.StringIO()

    df.to_csv(stream, index=False)

    response = StreamingResponse(iter([stream.getvalue()]), media_type='text/csv')

    response.headers['Content-Disposition'] = "attachment; filename=my_awesome_report.csv"

    return response


@app.get("/suma/")
def suma(Value1: float, Value2: float):
    return Value1 + Value2

@app.get("/resta/")
def resta(Value1: float, Value2: float):
    return Value1 - Value2

@app.get("/multiplicacion/")
def multiplicacion(Value1: float, Value2: float):
    return Value1 * Value2

@app.get("/division/")
def division(Value1: float, Value2: float):
    return Value1 / Value2


class  operaciones(BaseModel):
    Value1: float
    Value2: float

@app.post("/suma/")
async def suma(suma: operaciones):
    sum_dict = suma.dict()
    if suma.Value2:
        Suma = suma.Value1 + suma.Value2
        sum_dict.update({"Suma": Suma})
    return sum_dict

@app.post("/resta/")
async def resta(resta: operaciones):
    res_dict = resta.dict()
    if resta.Value2:
        Resta = resta.Value1 - resta.Value2
        res_dict.update({"Resta": Resta})
    return res_dict

@app.post("/multiplicacion/")
async def multiplicacion(multiplicacion: operaciones):
    multiplicacion_dict = multiplicacion.dict()
    if multiplicacion.Value2:
        Multiplicacion = multiplicacion.Value1 * multiplicacion.Value2
        multiplicacion_dict.update({"Multiplicacion": Multiplicacion})
    return multiplicacion_dict

@app.post("/division/")
async def division(division: operaciones):
    division_dict = division.dict()
    if division.Value2:
        Division = division.Value1 / division.Value2
        division_dict.update({"División": Division})
    return division_dict