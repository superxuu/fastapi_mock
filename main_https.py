import uvicorn
from fastapi import Depends, FastAPI, Header, HTTPException
from apis import create_app
from common.log_config import LOGGING_CONFIG
from fastapi.logger import logger

app = create_app()


@app.on_event("shutdown")
def shutdown_event():
    logger.info('shut down')


@app.on_event("startup")
async def startup_event2():
    logger.info('startup')


if __name__ == "__main__":
    # uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True, log_config=LOGGING_CONFIG, log_level='info', use_colors=True)
    uvicorn.run('main:app', host="0.0.0.0", port=8001, reload=True, log_config=LOGGING_CONFIG,
                log_level='info', ssl_keyfile = 'server.key', ssl_certfile = 'server.crt')
