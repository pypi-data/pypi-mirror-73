import time
import json

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import Response
from werkzeug.exceptions import abort

from mockspace.auth import login_required
from mockspace.db import get_db

bp = Blueprint("service", __name__)


@bp.route("/")
def index():
    """Show all the services, most recent first."""
    db = get_db()
    services = db.execute(
        "SELECT s.id, title, body, created, author_id, username"
        " FROM service s JOIN user u ON s.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()

    return render_template("service/index.html", services=services)


def get_service(id, check_author=True):
    """Get a service and by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of service to get
    :param check_author: require the current user to be the author
    :return: the service with author information
    :raise 404: if a service with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    service = (
        get_db()
            .execute(
            "SELECT s.id, title, body, created, author_id, username"
            " FROM service s JOIN user u ON s.author_id = u.id"
            " WHERE s.id = ?",
            (id,),
        )
            .fetchone()
    )

    if service is None:
        abort(404, "Service id {0} doesn't exist.".format(id))

    if check_author and service["author_id"] != g.user["id"] and service["author_id"] != 1:
        abort(403)

    return service


def get_service_by_title(title, check_author=False):
    """Get a service by title.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of service to get
    :param check_author: require the current user to be the author
    :return: the service with author information
    :raise 404: if a service with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    service = (
        get_db()
            .execute(
            "SELECT s.id, s.title, s.body, s.created, s.author_id, username"
            " FROM service s JOIN user u ON s.author_id = u.id"
            " WHERE s.title = ?",
            (title,),
        )
            .fetchone()
    )

    if service is None:
        abort(404, "Service '{0}' doesn't exist.".format(title))

    if check_author and service["author_id"] != g.user["id"]:
        abort(403)

    return service


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Create a new service for the current user."""
    if request.method == "POST":
        title = request.form["title"].replace(' ', '_')
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO service (title, body, author_id) VALUES (?, ?, ?)",
                (title, body, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("service.index"))

    return render_template("service/create.html")


@bp.route("/<string:service_name>/update", methods=("GET", "POST"))
@login_required
def update(service_name):
    """Update a service if the current user is the author."""
    service = get_service_by_title(service_name)

    if request.method == "POST":
        title = request.form["title"].replace(' ', '_')
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE service SET title = ?, body = ? WHERE id = ?", (title, body, service["id"])
            )
            db.commit()
            return redirect(url_for("service.index"))

    return render_template("service/update.html", service=service)


@bp.route("/<int:id>/delete", methods=("GET", "POST"))
@login_required
def delete(id):
    """Delete a service.

    Ensures that the service exists and that the logged in user is the
    author of the service.
    """
    get_service(id)
    db = get_db()
    db.execute("DELETE FROM service WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("service.index"))


@bp.route("/<string:service_name>", methods=("GET", "POST"))
def service(service_name):
    """Show all the methods, most recent first."""
    methods = []
    db = get_db()

    service = get_service_by_title(service_name)

    methods = db.execute(
        "SELECT m.id, title, body, status_code, delay, supported_method, created, author_id, username"
        " FROM method m JOIN user u ON"
        " m.author_id = u.id AND"
        " m.service_id = ?"
        " ORDER BY created DESC", (service["id"],),
    ).fetchall()

    return render_template("service/services.html", methods=methods, service_name=service_name, service=service)


def get_method(service_name, method_name, check_author=False):
    """Get a method by service_name, method_name.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of method to get
    :param check_author: require the current user to be the author
    :return: the method with author information
    :raise 404: if a method with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """

    method = (
        get_db()
            .execute(
            "SELECT m.id, m.title, m.body, m.status_code,"
            " m.delay, m.supported_method, m.headers,"
            " m.created, m.author_id, m.service_id, username"
            " FROM method m JOIN user u ON m.author_id = u.id"
            " JOIN service s ON m.service_id = s.id"
            " WHERE m.title = ? AND s.title = ?",
            (method_name, service_name),
        )
            .fetchone()
    )

    if method is None:
        abort(404, "Method {0} doesn't exist.".format(method_name))

    if check_author and method["author_id"] != g.user["id"]:
        abort(403)

    return method


def get_headers_from_request_form(request_form_data):
    """Gets form data, retrieves headers values and adds them to a tuple"""
    constant_form_fields = ['title', 'body', 'status_code', 'delay', 'supported_method']
    headers = {}

    # Python 3.7: Dictionary order is guaranteed to be insertion order. This is used to process dicts
    # The odd values of the source dictionary will become the keys of the header dictionary. Even - values.
    counter = 1
    for key, value in request_form_data.items():
        if key not in constant_form_fields:

            if counter % 2 != 0:
                headers_key = value
            else:
                headers_value = value
                headers[headers_key] = headers_value
            counter += 1

    # replacement of single by double quotes for further conversion of a string into a dictionary
    headers = str(headers).replace("'", "\"")

    return headers


@bp.route("/<string:service_name>/create_method", methods=("GET", "POST"))
@login_required
def create_method(service_name):
    """Create a new method for the current user, service."""
    if request.method == "POST":
        title = request.form["title"].replace(' ', '_')
        body = request.form["body"]
        status_code = int(request.form["status_code"])
        delay = int(request.form["delay"])
        supported_method = request.form["supported_method"]
        headers = get_headers_from_request_form(request.form)
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            service_id = db.execute(
                "SELECT id FROM service WHERE title = ?", (service_name,),
            ).fetchone()

            db.execute(
                "INSERT INTO method"
                " (title, body, status_code, delay, supported_method, headers, author_id, service_id)"
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (title, body, status_code, delay, supported_method, headers, g.user["id"], service_id['id']),
            )
            db.commit()
            return redirect(url_for("service.service", service_name=service_name))

    return render_template("service/create_method.html", service_name=service_name)


@bp.route("/<string:service_name>/<string:method_name>", methods=("GET", "POST", "PUT", "PATCH", "DELETE"))
def method(method_name, service_name):
    """Returns method response"""
    db = get_db()

    method = get_method(service_name, method_name)

    service = get_service_by_title(service_name)

    method_response = db.execute(
        "SELECT body, status_code, delay, supported_method, headers"
        " FROM method"
        " WHERE service_id = ? AND title = ?",
        (service["id"], method_name,),
    ).fetchone()

    body = method_response['body']
    status_code = method_response['status_code']
    delay = method_response['delay']
    supported_method = method_response['supported_method']
    headers = json.loads(method_response['headers'])

    if supported_method != request.method:
        return render_template("service/method_not_allowed.html", method=method, service_name=service_name,
                               method_name=method_name, current_method=request.method)

    # seconds to milliseconds
    delay = delay / 1000
    time.sleep(delay)

    return Response(body, status=status_code, headers=headers)


@bp.route("/<string:service_name>/<string:method_name>/update_method", methods=("GET", "POST"))
@login_required
def update_method(service_name, method_name):
    """Update a method if the current user is the author."""
    method = get_method(service_name, method_name)

    if request.method == "POST":
        title = request.form["title"].replace(' ', '_')
        body = request.form["body"]
        status_code = int(request.form["status_code"])
        delay = int(request.form["delay"])
        supported_method = request.form["supported_method"]
        headers = get_headers_from_request_form(request.form)

        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE method"
                " SET title = ?, body = ?, status_code = ?,"
                " delay = ?, supported_method = ?, headers = ?"
                " WHERE id = ?",
                (title, body, status_code, delay, supported_method, headers, method['id'])
            )
            db.commit()

            return redirect(url_for("service.service", service_name=service_name))

    method = get_method(service_name, method_name)

    headers = json.loads(method['headers'])

    return render_template("service/update_method.html", method=method, service_name=service_name, headers=headers)


@bp.route("/<string:service_name>/<string:method_name>/delete_method", methods=("GET", "POST"))
@login_required
def delete_method(service_name, method_name):
    """Delete the method.

    Ensures that the method exists and that the logged in user is the
    author of the method.
    """
    method_for_delete = get_method(service_name, method_name)
    db = get_db()
    db.execute("DELETE FROM method"
               " WHERE title = ? AND service_id = ?", (method_name, method_for_delete['service_id']))
    db.commit()

    return redirect(url_for("service.service", service_name=service_name))
