"""
Flask JWT Trivial.

Do not use this. Use Flask JWT Extended instead: https://github.com/vimalloc/flask-jwt-extended

Very basic functions and a decorator for Flask that provide some JavaScript Web Tokens functions.
"""

# Based on Flask_JWT_Extended, PyJWT and
# https://auth0.com/docs/quickstart/backend/python/01-authorization
# This is re-implemented in order to take advantage
# of modern crypto libraries, specifically python-jose.
# A very minimal subset of the functionality that
# python-jose provides is actually implemented.


from flask import current_app, request, abort
from functools import wraps
from http import HTTPStatus
from jose import jwt
from werkzeug import exceptions


class Flask_JWT_Trivial():
    def __init__(self,app=None,retfunc=None,passphrase=None,algorithms=["HS256","HS384","HS512"],algorithm="HS256",audience=None,issuer=None,subject=None):
        self.app = app
        self.retfunc = retfunc
        self.passphrase = passphrase
        self.algorithms = algorithms
        self.algorithm = algorithm
        self.audience = audience
        self.issuer = issuer
        self.subject = subject

    def init_app(self,app,**kwargs):
        self.__init__(app=app,**kwargs)


    def create_access_token(self,audience=None,issuer=None,subject=None):
        payload = {} 

        if audience:
            payload["aud"] = audience
        if issuer:
            payload["iss"] = issuer
        if subject:
            payload["sub"] = subject

        return jwt.encode(
            payload,
            self.passphrase,
            algorithm=self.algorithm
        )


    def jwt_required(self,audience=None,issuer=None,subject=None,
                     options={
                         "verify_signature": True,
                         "verify_aud": True,
                         "verify_iat": True,
                         "verify_exp": True,
                         "verify_nbf": True,
                         "verify_iss": True,
                         "verify_sub": True,
                         "verify_jti": True,
                         "verify_at_hash": True,
                         "leeway": 0}):

        if not audience:
            if self.audience:
                audience = self.audience
        if not issuer:
            if self.issuer:
                issuer = self.issuer
        if not subject:
            if self.subject:
                subject = self.subject


        def inner(f):
            @wraps(f)
            def decorated(*args,**kwargs):

                def _do_return(r):
                    if self.retfunc:
                        return self.retfunc(r)
                    else:
                        abort(exceptions.Unauthorized.code)

                auth_header = request.headers.get("Authorization", None)
                if not auth_header:
                    return _do_return(exceptions.Unauthorized)

                schema,token = None,None

                try:
                    schema,token = auth_header.split()
                except (AttributeError,ValueError) as e:
                    with self.app.app_context():
                        current_app.logger.error(e)
                    return self.retfunc(exceptions.Unauthorized)

                if not schema or not token or schema != "Bearer":
                    with self.app.app_context():
                        current_app.logger.error("JWT required with the schema 'Bearer'.")
                    return _do_return(exceptions.Unauthorized)

                # Check the token.
                try:
                    jwt.decode(token,self.passphrase,self.algorithms,audience=audience,issuer=issuer,subject=subject,options=options)
                except jwt.ExpiredSignatureError as e:
                    with self.app.app_context():
                        current_app.logger.error(e)
                    return _do_return(exceptions.Unauthorized)

                except jwt.JWTClaimsError as e:
                    with self.app.app_context():
                        current_app.logger.error(e)
                    return _do_return(exceptions.Unauthorized)

                except Exception as e:
                    with self.app.app_context():
                        current_app.logger.error(e)
                    return _do_return(exceptions.Unauthorized)

                # ?? _request_ctx_stack.top.current_user = token
                # See https://auth0.com/docs/quickstart/backend/python/01-authorization

                return f(*args,**kwargs)

            return decorated
        return inner
