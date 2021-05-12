import json
import logging
from rest_framework.renderers import JSONRenderer


logger = logging.getLogger(__name__)

class UserJSONRenderer(JSONRenderer):
    charset="utf-8"
    logger.info(
            "suis dans JSONrender"
        )

    def render(self, data, media_type=None, renderer_context=None):

        token = data.get('token', None)
        errors = data.get('errors', None)

        if token is not None and isinstance(token, bytes):
            data['token'] = token.decode('utf-8')
    
        if errors is not None: 
            return super(UserJSONRenderer, self).render(data)
        
        
        return json.dumps({
            'user': data
        })


