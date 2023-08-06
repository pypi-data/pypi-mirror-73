from functools import wraps
from holger.elasticsearch.client import ElasticSearchClient
import uuid
import datetime
from sentry_sdk import capture_event
from holger.sentry.utils.functions import config_scope, Level


def log(index: str, doc, params=None, headers=None):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            response, status_code = func(*args, **kwargs)
            status = response.get('status')
            metadata = response.get('metadata')
            created_at = datetime.datetime.now()
            client = ElasticSearchClient.get_client()
            elastic_response = client.index(
                index=index,
                body={
                    **response,
                    'created_at': created_at
                },
                doc_type=doc,
                id=metadata.get('id', uuid.uuid4()) if metadata else uuid.uuid4(),
                params=params,
                headers=headers
            )
            if status == 'failed':
                config_scope(metadata, status_code, Level.ERROR)
                sentry_exception_code = capture_event(
                    response.get('error')
                )
            elif status == 'success':
                config_scope(metadata, status_code, Level.INFO)
                sentry_exception_code = capture_event(
                    {
                        **response.get('data'),
                        'message': 'request was successfully submitted'
                    }
                )
            else:
                config_scope(metadata, status_code, Level.ERROR)
                sentry_exception_code = capture_event(
                    {
                        **response,
                        'message': F'status is invalid ({status})'
                    }
                )
            response.update({
                'elastic': {
                    **elastic_response,
                    'created_at': created_at
                },
                'sentry': {
                    'exception_code': sentry_exception_code,
                }
            })
            return response, status_code

        return inner

    return decorator
