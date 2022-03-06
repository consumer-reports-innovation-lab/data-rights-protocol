import os

import click
from fastapi import FastAPI
from pydantic import FilePath
from swagger_ui import api_doc
import uvicorn

# optional: plug in https://github.com/swagger-api/swagger-ui/blob/master/docs/usage/oauth2.md
# https://github.com/PWZER/swagger-ui-py#oauth2-configuration

app = FastAPI()
config_path = os.environ.get("DRP_OPENAPI", "openapi.yaml")
parms = dict()
api_doc(app, config_path=config_path, url_prefix='/swagger', title='DRP Requestor', parameters=parms)

@click.command(help="start the DRP swagger tool.")
@click.option("--host", "-h", help="the host IP to listen on, defaults to all IPs/interfaces", default="0.0.0.0")
@click.option("--port", "-p", help="port to listen on", default=8001)
def start(host="0.0.0.0", port=8001):
    click.echo(
        "swagger running on http://{}:{}/swagger ...".format(
            host,
            port
        ),
        err=True
    )
    uvicorn.run("datarightsprotocol.tools.swagger:app", host=host, port=port)
