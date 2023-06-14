from fastapi import Request


def get_param_from_request(param_name: str, request: Request):
    return request.query_params.get(param_name, '')
