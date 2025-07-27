from shared_utils.config_util import settings 
from shared_utils.logging_util import configure_logging
configure_logging(settings.log_level)

import os

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.logger import logger as fastapi_logger
from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from contextlib import asynccontextmanager

from shared_utils.migration_util import run_migrations
from api.user_routes import router as user_router
from api.found_item_routes import router as found_item_router
from api.requested_item_routes import router as requested_item_router

# Configure tracer provider with service name
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "gsalegig-api"})
    )
)

# Configure Jaeger exporter
oltp_exporter = OTLPSpanExporter(
    endpoint="http://localhost:4317"
)

# Add the exporter to the trace provider
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(oltp_exporter)
)

# Initialize the FastApi application
app = FastAPI()
FastAPIInstrumentor.instrument_app(app)

alembic_path = os.path.join(os.path.dirname(__file__), "alembic.ini")
run_migrations(alembic_path)

# Redundant assertion in startup, to override anything FastAPI/Uvicorn resets
@asynccontextmanager
async def lifespan(app: FastAPI):
    log_level = os.getenv("LOG_LEVEL", settings.log_level)
    configure_logging(log_level)
    yield  # App startup complete, continue normal operation

app = FastAPI(lifespan=lifespan)

import logging
fastapi_logger = logging.getLogger("app")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    fastapi_logger.error("422 Validation Error at %s", request.url.path)
    fastapi_logger.error("Request body: %s", await request.body())
    fastapi_logger.error("Validation errors: %s", exc.errors())
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

app.include_router(user_router)
app.include_router(found_item_router)
app.include_router(requested_item_router)

