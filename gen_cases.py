import models
import json
from hypothesis import given, strategies as st

safe_text = st.text(
    min_size=3,
    max_size=10,
    alphabet=st.characters(
        whitelist_categories=['L', 'P', 'N']
        #blacklist_categories=['C']
    )
)
simple_text = st.text(
    alphabet=st.characters(whitelist_categories=['L', 'N', 'P'])
)

id_strat = st.builds(
    models.IdentityPayload,
    iss=safe_text,
    aud=safe_text,
    sub=safe_text,
    name=safe_text,
    phone_number=simple_text,
    address=simple_text,
    power_of_attorney=simple_text,
)

strat = st.builds(
    models.DataRightsRequest,
    identity=id_strat,
    relationships=st.lists(
        st.text(
            min_size=3,
            max_size=10,
            alphabet=st.characters(
                blacklist_categories=['C']
            )
        ),
        min_size=0,
        max_size=10
    )
)

@given(strat)
def drr_identity_is_str(instance):
       exp = instance.as_json()
       tok = json.loads(exp)['identity']
       print(exp)
       assert(type(tok) == str)

print(strat.example().as_json())
print(json.dumps(id_strat.example().dict()))
