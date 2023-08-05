# Description

Gobits is a very small module, which acts as a metadata carrier for pub/sub messages. It automatically adds fields that may be useful downstream to determine the origin of a pub/sub message.

# Usage

Class attributes:

```python
class Gobits:
    """
    A small class that gathers information (bits) for a pub/sub message payload.

    Attributes:
        __request                Holds information about the cloud function request.
        __context                Holds information about the cloud function context.
        __message                The pub/sub message to be processed.
        _processed               Time of processing in milliseconds since epoch (UTC).
        _gcp_project             The source GCP project.
        _execution_id            The id of the execution.
        _execution_type          Type of the service processing the message.
        _execution_trigger_type  Type of the trigger invoking the processor.
        _function_name           Name of the processing cloud function.
        _function_version        Version of the processing cloud function.
        _event_id                The id of the trigger event.
        _message_id              The pub/sub message id.
        _message_publish_time    The time at which the message was published to pub/sub (UTC).
    """
```

Cloud function with HTTP trigger:

```python
from gobits import Gobits


def handler(request):

    envelope = json.loads(request.data.decode('utf-8'))
    message = envelope['message']['publishTime']

    bits = Gobits(request=request, message=message)

    message = {
      'gobits': bits.to_json(),
      'data': []
    }

```

Cloud function with storage trigger:

```python
from gobits import Gobits


def handler(data, context):

    bits = Gobits(context=context)

    message = {
      'gobits': bits.to_json(),
      'data': []
    }

```
