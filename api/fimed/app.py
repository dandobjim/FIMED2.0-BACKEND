import uvicorn
from fastapi import FastAPI
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response

from fimed import __version__
from fimed.config import settings
from fimed.logger import logger
from fimed.routes.authentication import router as auth_router
from fimed.routes.patient_crud import router as patient_router


app = FastAPI(
    title="FIMED",
    docs_url="/api/docs",
    openapi_prefix=settings.ROOT_PATH,
    description="https://github.com/dandobjim/FIMED2.0",
    version=__version__,
)

# cors

origins = ["*"]

app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

# routes


@app.get("/api/health", name="Health check", status_code=status.HTTP_200_OK, tags=["health"])
async def health():
    return Response(status_code=status.HTTP_200_OK)


app.include_router(auth_router, prefix="/api/v2/auth")
app.include_router(patient_router,prefix="/api/v2/patient")

def run_server():
    logger.info(f"🚀 Deploying server at http://{settings.API_HOST}:{settings.API_PORT}")
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT, root_path=settings.ROOT_PATH, log_level="info")



