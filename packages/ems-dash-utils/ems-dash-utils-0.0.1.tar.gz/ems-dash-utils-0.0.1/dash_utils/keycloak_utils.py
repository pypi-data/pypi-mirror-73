from flask import session, abort, make_response

KEYCLOAK_CLIENT = "asset-control"


def has_read_access(subject):

    try:
        for x in session["introspect"]["resource_access"][KEYCLOAK_CLIENT]["roles"]:
            if x == "admin":
                return True
            name, level = x.split("/")
            if name in ["ALL", subject] and level == "READ":
                return True
    except KeyError:
        return False
    return False


def has_write_access(subject):
    try:
        for x in session["introspect"]["resource_access"][KEYCLOAK_CLIENT]["roles"]:
            if x == "admin":
                return True
            name, level = x.split("/")
            if name in ["ALL", subject] and level == "WRITE":
                return True
    except KeyError:
        return False
    return False


def check_role(role):
    return role in session["introspect"]["resource_access"][KEYCLOAK_CLIENT]["roles"]


def require_role(roles: list):
    def inner(func):
        def wrapper(*args, **kwargs):
            if session["introspect"]["resource_access"][KEYCLOAK_CLIENT]["roles"] in roles:
                func(*args, **kwargs)
            else:
                abort(make_response(f"You do not have the required access", 401))
        return wrapper
    return inner
