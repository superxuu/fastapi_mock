from fastapi import FastAPI
from apis.test_api.api_operation import study1,study2
from apis.CIF_api.api_operation import bindcard,evalPhone
from apis.vba_api.api_operation import vba1,vba2

def create_app():

    app = FastAPI(title='FastApi Mock Server',
                  description='这是使用fastapi开发的挡板服务程序，旨在使用简单的操作实现快速可用的挡板服务',
                  version=0.1)



    app.include_router(
        study1.router,
        prefix="/items",
        tags=["items"],
        dependencies=[],
        responses={404: {"description": "Not found"}},
    )

    app.include_router(
        study2.router,
        prefix="/test",
        tags=["test"],
        dependencies=[],
        responses={404: {"description": "Not found"}},
    )


    app.include_router(
        bindcard.router,
        prefix="/bindcard",
        tags=["bindcard"],
        dependencies=[],
        responses={404: {"description": "Not found"}},
    )

    app.include_router(
        evalPhone.router,
        prefix="/evalPhone",
        tags=["evalPhone"],
        dependencies=[],
        responses={404: {"description": "Not found"}},
    )


    app.include_router(
        vba1.router,
        prefix="/vba1",
        tags=["vba1"],
        dependencies=[],
        responses={404: {"description": "Not found"}},
    )

    app.include_router(
        vba2.router,
        prefix="/vba2",
        tags=["vba2"],
        dependencies=[],
        responses={404: {"description": "Not found"}},
    )




    return app
