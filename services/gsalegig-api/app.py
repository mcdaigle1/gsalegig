from flask import Flask
from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor

import requests

# Configure tracer provider with service name
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "gsalegig-api"})
    )
)

# Configure Jaeger exporter
jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger-agent.monitoring.svc.cluster.local",  
    agent_port=6831,
)

# Add the exporter to the trace provider
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

# Initialize the Flask application
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

# Define a route for the root URL ("/")
@app.route('/')
def hello_world():
    # response = requests.get("http://name-generator-app-service/")
    # name = response.text
    
    # return 'Hello, World!' + name
    return 'Hello, World!'

# Run the app if this script is executed
if __name__ == '__main__':
    # Start the Flask web server
    app.run(debug=True, port=8080)