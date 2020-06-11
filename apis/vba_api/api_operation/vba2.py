from fastapi import APIRouter, Path, Query
from starlette.responses import FileResponse
from starlette.requests import Request
import logging
from common.mock_responce import MockResponce

router = APIRouter()


@router.post("/vvv/{url_path}")
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
    logging.info('json_body:', json_body)

    return FileResponse(MockResponce('vba_api', 'vba1', json_body).responce_filter(read=False))

