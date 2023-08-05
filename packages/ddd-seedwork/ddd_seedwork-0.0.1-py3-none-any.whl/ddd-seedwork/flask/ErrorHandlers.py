from flask import make_response, Flask

from src.domain.Exceptions import DomainError
from src.flask.ApiResponse import ApiResponse
from src.persistence.Exceptions import PersistenceError, NotFoundError


def register_errors(app: Flask):
    app.register_error_handler(DomainError, handle_domain_error)
    app.register_error_handler(PersistenceError, handle_persistence_error)
    app.register_error_handler(NotFoundError, handle_not_found_error)


def handle_domain_error(de):
    return make_response(ApiResponse(status="failed", message=de.__str__(), data=de.notifications).to_dict(),
                         400)


def handle_persistence_error(pe):
    return make_response(ApiResponse(status="failed", message=pe.__str__()).to_dict(), 400)


def handle_not_found_error(nfe):
    return make_response(ApiResponse(status="failed", message=nfe.__str__()).to_dict(), 404)
