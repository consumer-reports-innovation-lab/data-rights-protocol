from typing import TextIO
import click
import json
import os

from pydantic import FilePath

from models.core import DataRightsRequest
from models.identity import IdentityPayload
from tools.genjwts import generate as genjwts

def with_claims_from_stdin(drr: DataRightsRequest, input: TextIO) -> str:
    jwt_ser = input.read()
    click.echo("Read JWT... {}".format(jwt_ser), err=True)
    # being very lazy here; serialize it, deserialize it, replace the identity, serialize it... really??
    drr_ser = drr.json()
    reloaded = json.loads(drr_ser)
    reloaded["identity"] = jwt_ser
    return json.dumps(reloaded, indent=2)

def with_claims_from_generator(drr: DataRightsRequest, jwt: FilePath, secret: str) -> str:
    identity_payload = genjwts(template=jwt, override=[], verify=[])
    click.echo("Read JWT... {}".format(identity_payload), err=True)
    drr.identity = identity_payload
    return drr.json()

@click.command(help="Small utility function to generate a DataRightsRequest and serialize it.")
@click.option('--template', '-t', default="reqs/donotsell.json",
              help='DRR template to populate.',
              type=click.File('r'))
@click.option('--jwt', '-j',
              help="Generate a JWT using the specified template, otherwise read a serialized JWT from stdin (& probably out of genjwts.py)",
              type=click.File('r'),
              default="-")
def generate(template: TextIO, jwt: TextIO):
    click.echo("Constructing DRR against template `{}`.".format(template.name), err=True)
    tmpl = json.loads(template.read())

    drr = DataRightsRequest.construct(**tmpl)
    drr_ser = ""

    if jwt.name == "<stdin>":
        click.echo("Reading serialized JWT from stdin...", err=True)
        drr_ser = with_claims_from_stdin(drr, jwt)
        click.echo("Generating DRR:", err=True)
        click.echo(drr_ser)
    else:
        click.echo("Loading JWT", err=True)
        secret = os.environ.get("JWT_SECRET", "lolchangeme")
        jwt_filename = jwt.name
        drr_ser = with_claims_from_generator(drr, jwt_filename)
        click.echo("Generating DRR:", err=True)
        click.echo(drr_ser)

    return drr_ser


if __name__ == "__main__":
    generate()
