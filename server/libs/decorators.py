from pydantic import ValidationError
from libs.response import Response

_gateway_registry = []

def on(event_name):
    def decorator(func):
        setattr(func, "_socket_event", event_name)
        return func
    return decorator

def register_gateway(gateway_cls):
    _gateway_registry.append(gateway_cls)
    return gateway_cls

def get_registered_gateways():
    return _gateway_registry


def validate(model):
    def decorator(func):
        def wrapper(self, sid, data, *args, **kwargs):
            try:
                validated_data = model(**data)
            except ValidationError as e:
                return Response.error(f"Validation failed: {e}")

            return func(self, sid, validated_data, *args, **kwargs)
        
        return wrapper
    return decorator