# Flask JWT Trivial

*Pre-alpha, do not use!* Use [Flask JWT Extended](https://github.com/vimalloc/flask-jwt-extended) instead.


## About

Only bearer tokens are supported, no other methods.

The only valid algorithms for `create_access_token()` are `HS256`, `HS384`, or `HS512`. The default is `HS256`.


## Installation

Install into a virtual environment:

```
virtualenv --python python3 venv
source venv/bin/activate
pip install flask-jwt-trivial
```


## Example usage

First, generate a token and send it to the user. For them to access private routes, they must present that token as a bearer token, using the `Authorization` header, which will look something like this:

```
Authorization: Bearer <token-here>
```

Simple example follows. Note, it is up to you to manage the tokens, revoking them, checking expiry, etc.


```python
from flask import Flask, jsonify, abort
from flask_jwt_trivial import Flask_JWT_Trivial


app = Flask(__name__)

# Don't actually put this in your source code.
# Maybe read it from an environment variable.
passphrase = "VERY-SECRET-PASSPHRASE"

# Initialise your Flask app like so:
flask_jwt_trivial = Flask_JWT_Trivial()
flask_jwt_trivial.init_app(
    app,
    passphrase=passphrase
)

@app.route("/private")
@flask_jwt_trivial.jwt_required
def private():
    return "Your token worked."

def authorised_to_receive_a_token():
    # Put your logic here, e.g. check the Flask
    # request and look up details in a database.
    if ok:
        return True
    else:
        return False

@app.route("/get_token")
def get_token():
    if not authorised_to_receive_a_token():
        abort(401) # Unauthorized

    token = flask_jwt_trivial.create_access_token()

    return jsonify(
        "data": {
            "type": "tokens",
            "attributes": {
                "token": token,
                "category": "Bearer",
            }
        }
    )
```

Options for `flask_jwt_trivial.init_app()` are:

  - `app`: Compulsory first arg, the Flask app.
  - `algorithm`: Optional. String. Algorithm used to encode/decode. Defaults to `"HS256"`.
  - `algorithms`: Optional. List. Valid algorithms. Defaults to `["HS256","HS384","HS512"]`.
  - `audience`: Optional. String. JWT `aud` parameter.
  - `issuer`: Optional. String. JWT `iss` parameter, e.g. your organisation.
  - `retfunc`: Optional. A function that will be called on return. Useful if you want to capture the returned data and do something with it first.
