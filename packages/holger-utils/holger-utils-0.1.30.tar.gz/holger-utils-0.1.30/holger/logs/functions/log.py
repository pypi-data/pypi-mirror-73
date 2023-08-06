from holger.elasticsearch.client import ElasticSearchClient
import uuid
import datetime
from sentry_sdk import capture_event
from holger.sentry.utils.functions import config_scope, Level


def log(response, status_code, index: str, doc, params=None, headers=None):
    status = response.get('status')
    metadata = response.get('metadata')
    transaction = metadata.pop('transaction', {})
    created_at = datetime.datetime.now()
    client = ElasticSearchClient.get_client()
    elastic_id = metadata.get('id', F"{uuid.uuid4()}-{created_at.timestamp()}")
    client.index(
        index=index,
        body={
            **response,
            'transaction': transaction,
            'created_at': created_at
        },
        doc_type=doc,
        id=elastic_id,
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
    metadata.update({
        'transaction': {
            'elastic_id': elastic_id,
            'sentry_code': sentry_exception_code
        }
    })
