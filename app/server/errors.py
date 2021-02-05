from . import api


@api.app_errorhandler(404)
def page_not_found(e):
    return {
        "code": 404
    }
