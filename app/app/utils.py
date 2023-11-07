import json
from typing import Dict, Any

from fastapi_sso.sso.base import OpenID


def dumps(d):
    return json.dumps(d, ensure_ascii=False)


def convert_openid(response: Dict[str, Any]) -> OpenID:
    return OpenID(display_name=response['sub'])
