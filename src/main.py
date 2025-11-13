from mangum import Mangum
import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from exceptions import register_error_handlers
from routers.auth import router as authentication_router
from routers.accounts import router as account_router
from routers.realms import router as realm_router


app = FastAPI(title='Helheim Backend',
              version='0.1.0',
              debug=True
              )

app.add_middleware(CORSMiddleware,
                   allow_origins=settings.CORS_ORIGINS,
                   allow_methods=['GET', 'HEAD', 'OPTIONS',
                                  'POST', 'DELETE', 'PATCH'],
                   allow_credentials=True,
                   allow_headers=['*']
                   )


@app.get("/", tags=["root"])
async def get_root():
    return JSONResponse(status_code=200, content="It's Alive!")

app.include_router(authentication_router)
app.include_router(account_router)
app.include_router(realm_router)

register_error_handlers(app)

lambda_handler = Mangum(app, lifespan="off")
