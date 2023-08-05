import os
import time

from werkzeug.local import LocalProxy


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

    def __init__(self, request: LocalProxy = None, message: dict = None, context=None):
        self.__request = request
        self.__context = context
        self.__message = message
        self._processed = None
        self._gcp_project = None
        self._execution_id = None
        self._execution_type = None
        self._execution_trigger_type = None
        self._function_name = None
        self._function_version = None
        self._event_id = None
        self._message_id = None
        self._message_publish_time = None

    @property
    def request(self):
        return self.__request

    @request.setter
    def request(self, value):
        self.__request = value

    @property
    def context(self):
        return self.__context

    @context.setter
    def context(self, value):
        self.__context = value

    @property
    def message(self):
        return self.__message

    @message.setter
    def context(self, value):
        self.__message = value

    @property
    def processed(self):
        return str(int(round(time.time() * 1000)))

    @processed.setter
    def processed(self, value):
        self._processed = value

    @property
    def gcp_project(self):
        return os.getenv('X_GOOGLE_GCP_PROJECT')

    @gcp_project.setter
    def gcp_project(self, value):
        self._gcp_project = value

    @property
    def execution_id(self):
        if self.__request:
            return self.__request.headers.get('Function-Execution-Id')

    @execution_id.setter
    def execution_id(self, value):
        self._execution_id = value

    @property
    def execution_type(self):
        if os.getenv('X_GOOGLE_FUNCTION_NAME'):
            return 'cloud_function'

    @execution_type.setter
    def execution_type(self, value):
        self._execution_type = value

    @property
    def execution_trigger_type(self):
        return os.getenv('FUNCTION_TRIGGER_TYPE')

    @execution_trigger_type.setter
    def execution_trigger_type(self, value):
        self._execution_trigger_type = value

    @property
    def function_name(self):
        return os.getenv('X_GOOGLE_FUNCTION_NAME')

    @function_name.setter
    def function_name(self, value):
        self._function_name = value

    @property
    def function_version(self):
        return os.getenv('X_GOOGLE_FUNCTION_VERSION')

    @function_version.setter
    def function_version(self, value):
        self._function_version = value

    @property
    def event_id(self):
        if self.__context:
            return self.__context.event_id

    @event_id.setter
    def event_id(self, value):
        self._event_id = value

    @property
    def message_id(self):
        if self.__message:
            return self.__message.get('messageId')

    @message_id.setter
    def message_id(self, value):
        self._message_id = value

    @property
    def message_publish_time(self):
        if self.__message:
            return self.__message.get('publishTime')

    @message_publish_time.setter
    def message_publish_time(self, value):
        self._message_publish_time = value

    def to_json(self):

        protected = {k: v for (k, v) in self.__dict__.items() if '__' not in k}
        vars = {k.strip('_'): v for (k, v) in protected.items()}

        return vars
