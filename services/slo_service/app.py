import os
import requests
import logging

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from shared_utils.logging_util import configure_logging
import logging

from shared_utils.config_util import settings  # to initialize the settings values
from api.slo_routes import router as slo_router

# Configure tracer provider with service name
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "slo-service"})
    )
)

# Configure Jaeger exporter
otlp_exporter = OTLPSpanExporter(
    endpoint="jaeger-agent.monitoring.svc.cluster.local:6831",  
    insecure=True
)

# Add the exporter to the trace provider
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)

# Initialize the Flask application
app = FastAPI()
FastAPIInstrumentor.instrument_app(app)

configure_logging()
logger = logging.getLogger("slo_service.app")

app.include_router(slo_router)

# # Run the app if this script is executed
# if __name__ == '__main__':
#     # Start the Flask web server
#     app.run(debug=True, port=8080)