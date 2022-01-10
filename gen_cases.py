import models
import json
from hypothesis import given, strategies as st

@given(st.builds(models.DataRightsRequest))
def drr_identity_is_str(instance):
       exp = instance.as_json()
       tok = json.loads(exp)['identity']
       print(exp)
       assert(type(tok) == str)

drr_identity_is_str()
