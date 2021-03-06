import json

from rest_framework.renderers import JSONRenderer

class ArticleJSONRenderer(JSONRenderer):
    charset = 'utf8'

    def render(self, data, media_type=None, renderer_context=None):
        if data is not None:
            if len(data)<=1:
                return json.dumps({
                    'article':data
                })
            return json.dumps({
                'articles': data
            })
        return json.dumps({
            'article': 'No article found'
        })

