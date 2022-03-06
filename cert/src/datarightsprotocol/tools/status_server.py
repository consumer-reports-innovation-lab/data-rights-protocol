from uuid import UUID
import pathlib
import datetime
import json
import click

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseSettings, DirectoryPath

from datarightsprotocol.models import DataRightsStatus

class Settings(BaseSettings):
    drp_request_cache: DirectoryPath = "./drp-request-cache"

settings = Settings()
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <h1>Data Rights Protocol Status Callback Server</h1>

    <a href="/docs">Open Swagger</a>.
    """

@app.get("/show/{request_id}")
def read_request_statuses(request_id: UUID):
    # deserialize and return
    cache_path = settings.drp_request_cache
    cache_path = cache_path.joinpath(str(request_id))
    entries = [ json.loads(path.read_text()) for path in cache_path.glob("*.json") ]

    return entries

@app.post("/status_callback/{request_id}")
def process_status_callback(request_id: UUID, status: DataRightsStatus):
    """
    persist status to a file in json
    """

    request_time = datetime.datetime.now()
    cache_path = settings.drp_request_cache

    cache_path.joinpath(str(request_id)).mkdir()

    request_path = cache_path.joinpath(
        str(request_id),
        request_time.strftime("%s.json")
    )

    request_path.write_text(status.json())

    return request_path

import uvicorn

@click.command(help="start the DRP status servlet")
@click.option("--host", "-h", help="the host IP to listen on, defaults to all IPs/interfaces", default="0.0.0.0")
@click.option("--port", "-p", help="port to listen on", default=8000)
def start(host="0.0.0.0", port=8000):
    uvicorn.run("datarightsprotocol.tools.status_server:app", host=host, port=port)
    
