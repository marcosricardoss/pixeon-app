"""This module registers the error handler on the application."""


from flask import make_response, jsonify


def register_handler(app):
    """Registers the error handler is a function to common error HTTP codes

    Parameters:    
    app (flask.app.Flask): The application instance.
    """

    @app.errorhandler(400)
    def bad_request(error):
        """Deal with HTTP BadRequest exceptions.

        Parameters:
        error (BadRequest): A werkzeug.exceptions.BadRequest exception object.

        Returns:
        A flask response object.
        """

        return make_response(jsonify({
            'status': 'error',
            'message': 'Bad request'
        }), 400)

    @app.errorhandler(401)
    def bad_request(error):
        """Deal with HTTP Unauthorized exceptions.

        Parameters:
        error (Unauthorized): A werkzeug.exceptions.Unauthorized exception object.

        Returns:
        A flask response object.
        """

        return make_response(jsonify({
            'status': 'error',
            'message': 'Missing authorization header'
        }), 401)

    @app.errorhandler(404)
    def not_found(error):
        """ Deal with HTTP NotFound exceptions.

        Parameters:
        error (NotFound): A werkzeug.exceptions.NotFound exception object.

        Returns:
        A flask response object.
        """

        return make_response(jsonify({
            'status': 'error',
            'message': 'Not found'
        }), 404)


    @app.errorhandler(405)
    def method_not_allowed(error):
        """ Deal with HTTP MethodNotAllowed exceptions.

        Parameters:
        error (MethodNotAllowed): A werkzeug.exceptions.MethodNotAllowed exception object.

        Returns:
        A flask response object.
        """

        return make_response(jsonify({
            'status': 'error',
            'message': 'Method not allowed'
        }), 405)

    @app.errorhandler(409)
    def not_found(error):
        """ Deal with HTTP Conflict exceptions.

        Parameters:
        error (NotFound): A werkzeug.exceptions.Conflict exception object.

        Returns:
        A flask response object.
        """

        return make_response(jsonify({
            'status': 'error',
            'message': 'State conflict'
        }), 409)

    @app.errorhandler(429)
    def not_found(error):
        """ Deal with HTTP TooManyRequests exceptions.

        Parameters:
        error (NotFound): A werkzeug.exceptions.TooManyRequests exception object.

        Returns:
        A flask response object.
        """

        return make_response(jsonify({
            'status': 'error',
            'message': 'Too Many Requests'
        }), 429)

    @app.errorhandler(500)
    def internal_server_error(error):
        """ Deal with HTTP InternalServerError exceptions.

        Parameters:
        error (MethodNotAllowed): A werkzeug.exceptions.InternalServerError exception object.

        Returns:
        A flask response object.
        """

        return make_response(jsonify({
            'status': 'fail',
            'message': 'Internal server error'
        }), 500)