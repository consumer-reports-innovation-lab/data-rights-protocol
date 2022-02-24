import os
import json

from models.identity import IdentityPayload, IdentityClaims
from models import BaseModel

from pydantic import FilePath
from typing import List
import click

VERIFIABLE_CLAIMS = [
    IdentityClaims.email,
    IdentityClaims.address,
    IdentityClaims.name_,
    IdentityClaims.phone_number
]

@click.command(help="Small utility function to generate an IdentityPayload and serialize it.")
@click.option('--secret', '-s', default="lolchangeme",
              help="JWT HS256 signing key")
@click.option('--template', '-t', default="jwts/simple.json",
              help="JWT template to populate")
@click.option('--override', '-o', default=[], multiple=True,
              help="specify overrides to the JWT template in the form of 'claim=val'. can be specified repeatedly.")
@click.option('--verify', '-v', default=[], multiple=True,
              help="specify claims to mark as 'verified'.")
def generate(secret: str,
             template: FilePath,
             override: List[str],
             verify: List[str]):
    os.environ['JWT_SECRET'] = secret

    click.echo("Constructing claim.", err=True)
    tmpl = None
    with open(template) as f:
        tmpl = json.loads(str(f.read()))

    overrides = [pair.split("=") for pair in override]
    click.echo("Overriding template: {}".format(overrides), err=True)
    for (claim, value) in iter(overrides):
        tmpl[claim] = value

    pl = IdentityPayload(**tmpl)

    click.echo("Verifying claims: {}".format(verify), err=True)
    for claim in verify:
        if claim == "email":
            pl.verified_email = True
        elif claim == "phone_number":
            pl.verified_phone_number = True
        elif claim == "address":
            pl.verified_address = True
        else:
            raise Exception("Cannot mark '{}' as verified".format(claim))

    encoded = pl.json()
    click.echo("Your JWT has arrived.", err=True)
    click.echo(encoded)
    

if __name__ == "__main__":
    generate()
