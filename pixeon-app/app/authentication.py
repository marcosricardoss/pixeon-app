"""Initialize the JWTManager by setting functionality to manage the token."""

from flask import make_response, jsonify

def init_authentication(jwt):
    """Initialize the JWTManager.
    
    Parameters:    
        jwt (JWTManager): an instance of the jwt manager.
    """

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decoded_token):
        """Callback to check if a token is in the blacklist.
        
        Parameters:    
            decrypted_token (dict): a jwt token decrypted into a dictionary.
        """
        
        pass

    @jwt.unauthorized_loader  
    def my_unauthorized_loader(error):
        return make_response(jsonify({
            "status": "error",
            "message": error
        }), 401)