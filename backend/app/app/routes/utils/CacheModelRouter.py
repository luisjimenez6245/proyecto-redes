from fastapi_helpers import DefaultModelRouter, Pagination
from db.redis import cache
from fastapi import (
    Request,Depends,
    HTTPException, Response, status
)
from core.logger import logger
from typing import Dict, Optional, Union, List, Any
from ormar import Model
from orjson import dumps

class CacheModelRouter(DefaultModelRouter):

    cache_key_format = "{model_name}:{action}:{id}"
    actions = ["get", "list"]

    def __init__(self, model, crud):
        super().__init__(model, crud)

    async def read(self, id: Optional[Union[int, str]]) -> Union[Optional[Model] , Dict]:
        key = self.cache_key_format.format(model_name=self.model.__name__, action="get", id=str(id))
        key = key.replace(" ", "")
        data =  cache.get(key)
        if(data):
            logger.info(f"Cache hit for {key}")
            return Response(data, status.HTTP_200_OK, self.headers)
        m = await self.crud.get(id=id)
        if(m is None):
            raise HTTPException(404, self.NOT_FOUND_ERR, self.headers)
        if(isinstance(m, Model)):
            cache.set(key, dumps(m.dict()))
            return Response(dumps(m.dict()), status.HTTP_200_OK, self.headers)
        cache.set(key, dumps(m))
        return Response(dumps(m), status.HTTP_200_OK, self.headers)

    
    async def read_list(
        self,
        *,
        request: Request,
        options: Pagination = Depends(),
    ):
        key = self.cache_key_format.format(model_name=self.model.__name__, action="list", id=request.query_params)
        key = key.replace(" ", "")
        data = cache.get(key)
        if(data):
            logger.info(f"Cache hit for {key}")
            return Response(data, status.HTTP_200_OK, self.headers)
        options.set_filters(**request.query_params._dict)
        r = await self.crud.get_list(options)
        cache.set(key, dumps(r))
        return r