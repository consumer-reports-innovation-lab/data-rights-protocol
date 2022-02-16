import jwt

from models import IdentityPayload

import click

@click.command(help="Small utility function to generate an IdentityPayload and serialize it.")
@click.option('--secret', default="lolchangeme", help="JWT HS256 signing key")
@click.option('--iss', default="drp-test", help="JWT iss Field")
@click.option('--aud', default="the-pip", help="JWT aud Field")
@click.option('--sub', default="the-consumer", help="JWT sub Field")
@click.option('--email', help="JWT email Field")
@click.option('--phone', help="JWT phone_number Field")
@click.option('--address', help="JWT address Field")
@click.option('--poa-id', help="JWT power_of_attorney Field")
def generate(iss: str,
             aud: str,
             sub: str,
             email: str,
             phone: str,
             address: str,
             poa_id: str,
             secret: str):
    constructed = models.IdentityPayload(
        )
    pass

if __name__ == "__main__":
    generate()
