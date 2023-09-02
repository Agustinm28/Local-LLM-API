from functools import wraps
from flask import request, jsonify
import json
import secrets
import string

def require_api_key(view_func):
    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        api_key = request.headers.get("Authorization")

        with open('data/api_keys.json', 'r') as f:
            api_keys = json.load(f)

        if api_key and api_key in api_keys.values():
            return view_func(*args, **kwargs)
        else:
            return jsonify({"message": "Unauthorized"}), 401
    
    return decorated_view

def require_master_key(view_func):
    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        master_key = request.headers.get("Authorization")

        with open('data/master_key.json', 'r') as f:
            master_dict = json.load(f)

        if master_key and master_key in master_dict.values():
            return view_func(*args, **kwargs)
        else:
            return jsonify({"message": "Unauthorized"}), 401
    
    return decorated_view

def generate_api_key():
    
    alphabet = string.ascii_letters + string.digits
    api_key = ''.join(secrets.choice(alphabet) for i in range(20))

    with open('data/api_keys.json', 'r') as f:
        api_keys = json.load(f)

    # Get the las key value and increment it by 1
    if len(api_keys) == 0:
        api_key_number = 1
    else:
        api_key_number = list(api_keys.keys())[-1]
        api_key_number = int(api_key_number) + 1
        api_key_number = str(api_key_number)
        print(api_key_number)

    api_keys[api_key_number] = api_key

    with open('data/api_keys.json', 'w') as f:
        json.dump(api_keys, f, indent=4)

    return api_key