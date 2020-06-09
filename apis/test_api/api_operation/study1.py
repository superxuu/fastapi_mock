import time

from fastapi import APIRouter, Path, Query
from starlette.responses import FileResponse
from starlette.requests import Request

from common.mock_responce import MockResponce
# from common.log_config import getloger

router = APIRouter()
# logger = getloger(__name__)

@router.post("/v1/{url_path}")
async def json_res(request: Request, url_path=Path(..., title="The ID of the item to get")):
    print(request.url)

    # query_args = request.query_params
    # logger.info('query_args:', query_args)
    # logger.info(query_args.get('entInfo'))

    # form_args = await request.form()
    # print('form_args:', form_args)
    # print(form_args.get('entInfo'))

    # byte_body = await request.body()
    # try:
    #     import json
    #     b_body = json.loads(byte_body.decode('UTF-8'))
    #     print('byte_body:', b_body)
    #     print(type(b_body))
    # except:
    #     b_body = byte_body.decode('UTF-8')
    #     print('byte_body:', b_body)
    #     print(type(b_body))

    json_body = await request.json()


    return FileResponse(MockResponce('test_api', 'A001', json_body).responce_filter())


@router.post("/v1/txt")
async def txt_res(request: Request):
    form_args = await request.form()
    return FileResponse(MockResponce('test_api', 'A002', form_args).responce_filter())
