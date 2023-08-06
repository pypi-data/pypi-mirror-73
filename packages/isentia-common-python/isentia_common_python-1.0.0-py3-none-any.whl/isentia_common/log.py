import logging
import re
import sys

from pythonjsonlogger import jsonlogger


def _modified_jsonlogger_merge_record(namespace):
    def custom_func(record, target, reserved):
        """
        Merges extra attributes from LogRecord object into target dictionary

        :param record: logging.LogRecord
        :param target: dict to update
        :param reserved: dict or list with reserved keys to skip

        Customized the function to nest the non standard log properties
        inside another json object with field name set as the namespace
        name. Log format will come out as the following if namespace="my-app":
        {
            "name": "root",
            "levelname": "INFO"
            "my_app": {
                "example_key1": ...,
                "example_key2": ...,
                ...
            }
            "global": {
                "example_key3": ...,
                "example_key4": ...,
                ...
            }
        }
        """
        ns_dict = {}
        for key, value in record.__dict__.items():
            if key is "global" and isinstance(value, dict):
                target[key] = value

            # this allows to have numeric keys
            elif key not in reserved and not (hasattr(key, "startswith") and key.startswith("_")):
                ns_dict[key] = value

        # nest the fields in a defined namespace so it's
        # easier to manage index patterns in Kibana
        if ns_dict:
            target[namespace] = ns_dict
        return target

    return custom_func


def init_json_logging(namespace, extended=False):
    """ Configures formatting of logging (all levels) 
    to log in json """
    if namespace is None:
        raise EnvironmentError("Must set a namespace!")

    match = re.search("^[A-Za-z_-]+$", namespace)
    if not match:
        raise EnvironmentError(
            f"'{namespace}' is not valid. Please use names with letters, hyphens and underscores."
        )

    if namespace.lower() == "global":
        raise EnvironmentError(
            "'global' namespace is already reserved, please choose another name."
        )

    ns = namespace.replace("-", "_").lower()

    # Since we decided not to fork the jsonlogger library, we need to
    # monkey patch the function 'merge_record_extra' with our own implementation.
    # Please be wary of future version upgrade to python-json-logger by
    # making sure the custom function doesn't differ in signature from
    # jsonlogger.merge_record_extra
    jsonlogger.merge_record_extra = _modified_jsonlogger_merge_record(ns)

    root_logger = logging.getLogger()

    # remove existing log handlers from
    # python logging library, if any
    for h in root_logger.handlers:
        root_logger.removeHandler(h)

    log_handler = logging.StreamHandler()

    if extended:
        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(name)s %(levelname)s %(message)s %(process)i %(filename)s %(lineno)s %(funcName)s"
        )
    else:
        formatter = jsonlogger.JsonFormatter("%(asctime)s %(name)s %(levelname)s %(message)s")

    log_handler.setFormatter(formatter)

    # add json log handler and set log level
    root_logger.addHandler(log_handler)
    root_logger.setLevel(logging.INFO)

    sys.excepthook = _unhandled_exception


def _unhandled_exception(exc_type, exc_value=None, exc_traceback=None, err_msg=None, object=None):
    logging.exception("Unhandled exception", exc_info=exc_value)
