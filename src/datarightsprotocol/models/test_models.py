import jwt
import json

import models

def test_DRR_init():
    jwt_audience = 'pip'
    drr = models.DataRightsRequest(
        exercise=[models.Action.opt_out],
        identity=models.IdentityPayload(
            iss='ryan',
            sub='dazza',
            aud=jwt_audience,
            name='dazza',
            email='dazza@civics.com',
            verified_email=True
        )
    )

    assert type(drr.json()) == str, "json returns a str"
    assert drr.identity.dict().get("iss") == "ryan", "issuer in identity payload"
    assert drr.identity.dict().get("email_verified") == "dazza@civics.com", "verified cred in identity payload"

    reloaded = json.loads(drr.json())

    assert type(reloaded["identity"]) == str
    assert "regime" in  reloaded.keys()
    assert "exercise" in  reloaded.keys()
    assert reloaded["exercise"][0] == models.Action.opt_out

    settings = models.base.settings
    decoded = jwt.decode(
        reloaded["identity"],
        settings.jwt_secret,
        algorithms=settings.jwt_algo,
        audience=jwt_audience
    )

    assert decoded["iss"] == "ryan", "decoded jwt contains fields"
    assert decoded["email_verified"] == "dazza@civics.com", "decoded jwt contains verified fields"

