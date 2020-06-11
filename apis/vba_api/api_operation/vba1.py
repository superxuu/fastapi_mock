from starlette.responses import Response
from fastapi import APIRouter, Path, Query
from starlette.responses import FileResponse
from starlette.requests import Request
from common.mock_responce import MockResponce
import logging

router = APIRouter()

@router.post("/vvv/{url_path}")
async def json_res(request: Request, url_path=Path(..., title="The ID of the item to get")):
    """性能模式"""
    json_body = await request.json()
    logging.info(f'json_body:{json_body}')
    return Response(MockResponce('vba_api', 'vba1', json_body).responce_filter(read=True), media_type='application/json')



@router.post("/bbb/txt")
async def txt_res(request: Request):
    """非性能模式"""
    query_args = request.query_params
    return FileResponse(MockResponce('vba_api', 'vba1', query_args).responce_filter(read=False))
