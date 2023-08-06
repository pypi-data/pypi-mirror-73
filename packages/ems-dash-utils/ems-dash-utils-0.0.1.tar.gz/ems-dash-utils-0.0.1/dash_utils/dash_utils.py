from datetime import datetime

import pytz
from dash import callback_context, Dash
from flask import request
import os

CLIENT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def init_client_tz_javascript(dashapp: Dash):
    """
    Initializes a snippet of javascript which saves a cookie with the timezone of the client
    :param dashapp: The Dash app object
    """
    path = dashapp.config.get("assets_folder", "assets")

    if not os.path.exists(path):
        os.mkdir(path)
    with open(os.path.join(path, "timezone.js"), "w+") as f:
        f.write("document.cookie = 'tz=' + Intl.DateTimeFormat().resolvedOptions().timeZone;")


def get_client_tz() -> datetime.tzinfo:
    """
    Retrieves the timezone of the client, if it has been initialized. Otherwise returns UTC
    :return: The client timezone
    """
    return pytz.timezone(request.cookies.get("tz", "UTC"))


def to_client_tz(dt: datetime) -> datetime:
    """
    Transforms a datetime to the client timezone. Defaults to UTC if it has not been initialized.
    :param dt: A Datetime object
    :return: A datetime object localized in the client timezone
    """
    return dt.astimezone(get_client_tz())


def parse_client_date(s: str) -> datetime:
    """
    Parses a datetime and localizes it to the client timezone
    :param s: A string
    :return: A datetime object
    """
    dt = datetime.strptime(s, CLIENT_DATE_FORMAT)
    return get_client_tz().localize(dt)


def format_client_date(dt: datetime) -> str:
    """
    Formats a datetime object with a given format, in the clients timezone.
    :param dt: A datetime object
    :return: A string
    """
    tz = pytz.timezone(request.cookies.get("tz", "UTC"))
    return dt.astimezone(tz).strftime(CLIENT_DATE_FORMAT)


def was_source(name: str) -> bool:
    """
    Checks whether a given id triggered the callback
    :param name: Id of component
    :return: True if it was triggered by the given id
    """
    ctx = callback_context

    return ctx.triggered and  \
           ctx.triggered[0]['prop_id'].split('.')[0] == name


def get_source():
    """
    Returns the id of the object which triggered the callback
    :return: The id
    """
    ctx = callback_context

    return ctx.triggered[0]['prop_id'].split('.')[0]


