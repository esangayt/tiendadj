from rest_framework.renderers import JSONRenderer
from django.conf import settings


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get('response')
        response_status = response.status_code if response else 200
        response_data = {
            "error": not 200 <= response_status < 300,
            # 'message': response.status_text,
            'message': data.get('message', ''),
            "code": response.status_code,
            'data': data if 200 <= response_status < 300 else None
        }

        if response_status >= 400 and settings.DEBUG:
            response_data.update({
                'debug' : data['debug']
            })

        #pagination
        # if 'count' in data and 'results' in data:
        #     # print('entro')
        #     response_data.update({
        #         'count': data['count'],
        #         "next": data['next'],
        #         "previous": data['previous'],
        #         'data': data['results'],
        #     })

        return super().render(response_data, accepted_media_type, renderer_context)