from typing import TextIO, List
from collections.abc import Iterable
import click
import json
import os

from pydantic import FilePath

from datarightsprotocol.models.core import DataRightsRequest
from datarightsprotocol.models.identity import IdentityPayload
from datarightsprotocol.tools.genjwts import generate as genjwts

def with_claims_from_stdin(drr: DataRightsRequest, input: TextIO) -> str:
    '''
    Augment a partially-constructed DRR with a serialized JWT read from input, probably stdin.
    '''
    jwt_ser = input.read()
    click.echo("Read JWT... {}".format(jwt_ser), err=True)
    # being very lazy here; serialize it, deserialize it, replace the identity, serialize it... really??
    drr_ser = drr.json()
    reloaded = json.loads(drr_ser)
    reloaded["identity"] = jwt_ser
    return json.dumps(reloaded, indent=2)


def with_claims_from_generator(drr: DataRightsRequest, jwt: FilePath) -> str:
    '''
    Augment a partially constructed DRR with a JWT instantiated with a default-ish call to ./genjwts.py
    The JWT signing secret will need to be provided using JWT_SECRET environment variable to operationalize this.
    '''
    identity_payload = genjwts(template=jwt, override=[], verify=[])
    click.echo("Read JWT... {}".format(identity_payload), err=True)
    drr.identity = identity_payload
    return drr.json()


def generate(template: TextIO, jwt: TextIO, override: List[str]):
    click.echo("Constructing DRR against template `{}`.".format(template.name), err=True)
    tmpl = json.loads(template.read())

    overrides = [pair.split("=") for pair in override]
    has_overridden: set[str] = set()
    click.echo("Overriding template: {}".format(overrides), err=True)
    for (claim, value) in iter(overrides):
        if isinstance(tmpl[claim], Iterable):
            if claim in has_overridden:
                tmpl[claim].append(value)
            else:
                tmpl[claim] = [value]
        else:
            tmpl[claim] = value
        has_overridden.add(claim)

    drr = DataRightsRequest.construct(**tmpl)
    if jwt.name == "<stdin>":
        click.echo("Reading serialized JWT from stdin...", err=True)
        return with_claims_from_stdin(drr, jwt)
    else:
        click.echo("Loading JWT", err=True)
        secret = os.environ.get("JWT_SECRET", "lolchangeme")
        jwt_filename = jwt.name
        return with_claims_from_generator(drr, jwt_filename)


@click.command(help="Small utility function to generate a DataRightsRequest and serialize it.")
@click.option('--template', '-t', default="reqs/donotsell.json",
              help='DRR template to populate.',
              type=click.File('r'))
@click.option('--jwt', '-j',
              help="Generate a JWT using the specified template, otherwise read a serialized JWT from stdin (& probably out of genjwts.py)",
              type=click.File('r'),
              default="-")
@click.option('--override', '-o', default=[], multiple=True,
              help='''Specify overrides to DRR values.
              Values specified as a list will be overwritten on first override, then appended to after, if that makes sense.''')
def cmd(template: TextIO, jwt: TextIO, override: List[str]):
    click.echo("Generating DRR:", err=True)
    drr_ser = generate(template, jwt, override)
    click.echo(drr_ser)


if __name__ == "__main__":
    cmd()
