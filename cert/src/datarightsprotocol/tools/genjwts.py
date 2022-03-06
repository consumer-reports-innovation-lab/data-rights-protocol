import json

from datarightsprotocol.models.identity import IdentityPayload, IdentityClaims

from pydantic import FilePath
from typing import List
import click
import os

def generate(template: FilePath,
             override: List[str],
             verify: List[str]) -> IdentityPayload:
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
        if claim == IdentityClaims.email:
            pl.verified_email = True
        elif claim == IdentityClaims.phone_number:
            pl.verified_phone_number = True
        elif claim == IdentityClaims.address:
            pl.verified_address = True
        elif claim == IdentityClaims.name_:
            pl.verified_name = True
        else:
            raise Exception("Cannot mark '{}' as verified".format(claim))

    return pl
    

@click.command(help="Small utility function to generate an IdentityPayload and serialize it.")
@click.option('--secret', '-s', default="lolchangeme",
              envvar="JWT_SECRET",
              help="JWT HS256 signing key")
@click.option('--template', '-t', default="jwts/simple.json",
              help="JWT template to populate")
@click.option('--override', '-o', default=[], multiple=True,
              help="specify overrides to the JWT template in the form of 'claim=val'. can be specified repeatedly.")
@click.option('--verify', '-v', default=[], multiple=True,
              help="specify claims to mark as 'verified'.")
def cmd(secret: str,
        template: FilePath,
        override: List[str],
        verify: List[str]):
    ip = generate(template, override, verify)
    click.echo("", err=True)

    encoded = ip.json(secret=secret)
    click.echo("Your JWT has arrived.", err=True)
    click.echo(encoded)

    return encoded

if __name__ == "__main__":
    cmd()
