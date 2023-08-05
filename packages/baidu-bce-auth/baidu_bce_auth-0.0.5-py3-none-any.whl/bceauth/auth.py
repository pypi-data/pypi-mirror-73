# -*- coding: utf-8 -*-

import hashlib
import hmac
from datetime import datetime
from typing import List, Set, Tuple

from .utils import uri_encode, uri_encode_except_slash

BCE_PREFIX: str = 'x-bce-'


def make_auth(
    ak: str, sk: str, method: str, path: str,
    params: dict, headers: dict, headers_to_sign: Set[str] = None,
) -> str:
    canonical_uri = uri_encode_except_slash(path)
    canonical_query_string = _to_canonical_query_string(params)
    canonical_headers, signed_headers = _to_canonical_headers(
        headers, headers_to_sign)
    canonical_request = f'{method}\n{canonical_uri}\n{canonical_query_string}\n{canonical_headers}'  # noqa

    timestamp = _to_timestamp()

    auth_string_prefix = f'bce-auth-v1/{ak}/{timestamp}/1800'

    signing_key = hmac.new(
        sk.encode(),
        auth_string_prefix.encode(),
        hashlib.sha256).hexdigest()

    signature = hmac.new(
        signing_key.encode(),
        canonical_request.encode(),
        hashlib.sha256).hexdigest()

    return f'bce-auth-v1/{ak}/{timestamp}/1800/{signed_headers}/{signature}'


def _to_canonical_query_string(params: dict) -> str:
    param_list: List[str] = []
    for k, v in params.items():
        new_k = uri_encode(k)
        if v:
            new_v = uri_encode(str(v))
        else:
            new_v = ''
        param_list.append(f'{new_k}={new_v}')
    return '&'.join(sorted(param_list))


def _to_canonical_headers(
    headers: dict, headers_to_sign: Set[str] = None
) -> Tuple[str, str]:
    headers = headers or {}

    if headers_to_sign is None or len(headers_to_sign) == 0:
        headers_to_sign = {
            # 百度云只强制要求编码 "host" header
            'host',
        }
    else:
        headers_to_sign = {
            h.strip().lower()
            for h in headers_to_sign
        }

    result: List[str] = []
    signed_headers: Set[str] = set()
    for k, v in headers.items():
        k_lower = k.strip().lower()

        if k_lower.startswith(BCE_PREFIX) or k_lower in headers_to_sign:
            new_k = uri_encode(k_lower)
            new_v = uri_encode(str(v).strip())
            result.append(f'{new_k}:{new_v}')
            signed_headers.add(new_k)

    return '\n'.join(sorted(result)), ';'.join(sorted(signed_headers))


def _to_timestamp() -> str:
    t = datetime.utcnow().isoformat(timespec='seconds')
    return f'{t}Z'
