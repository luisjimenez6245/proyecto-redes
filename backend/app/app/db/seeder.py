from os import path
from core.logger import logger
from orjson import loads
from fastapi_helpers import BaseCrud
import crud

async def read_index(main_path="../seeds/", index_path="index.json"):
    index = open(path.join(main_path, index_path), "r")
    index_content = "".join(index.readlines())
    index.close()
    classes = loads(index_content)
    for cls in classes:
        fil = open(path.join(main_path, cls['name'] + ".json"), "r")
        fil_content = "".join(fil.readlines())
        fil.close()
        objects = loads(fil_content)
        crud_obj: BaseCrud = eval("crud." + cls['crud'])
        for obj in objects:
            await crud_obj.create(obj)
    return True

dependencies = [read_index]
dev_dependencies = []

async def db_fill():
    errors = []
    try:
        for d in dependencies:
            try:
                await d()
            except Exception as exx:
                errors.append({
                    'error': exx,
                    'obj' : d.__name__                    
                })
        for d in dev_dependencies:
            await d()
        return str(errors)
    except Exception as ex:
        return str(ex)
