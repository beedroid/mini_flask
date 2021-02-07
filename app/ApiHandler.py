from app.ApiUtils import ApiUtils

def api_handler_init_app(app, db):
    apiUtils = ApiUtils().init_app(app)
    @app.errorhandler(404)
    def not_found_error(error):
        return apiUtils.make_response_error(404, error.description)

    @app.errorhandler(405)
    def not_found_error(error):
        return apiUtils.make_response_error(405, error.description)

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return apiUtils.make_response_error(500, error.description)