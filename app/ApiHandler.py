from app.ApiUtils import *

def api_handler_init_app(app, db):
    @app.errorhandler(404)
    def not_found_error(error):
        return make_response_error(404, error.description)

    @app.errorhandler(405)
    def not_found_error(error):
        return make_response_error(405, error.description)

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return make_response_error(500, error.description)