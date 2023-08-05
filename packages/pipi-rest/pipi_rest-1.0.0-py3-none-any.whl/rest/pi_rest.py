import functools
import json
from pi_json.pi_json import PiJsonEncoder

class HandlerException(Exception):

  def __init__(self, **kwargs):
    self.__dict__.update(**kwargs)


def json_return(_func=None, *, encoder_cls=None):
  def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      rs = func(*args, **kwargs)
      return json.dumps(rs, cls=PiJsonEncoder if not encoder_cls else encoder_cls)
    return wrapper

  if _func is None:
    return decorator
  else:
    return decorator(_func)


def exception_handler(_func=None, *, exceptions=(), f_return=None, params=None, kwparam=None):

  if kwparam is None:
    kwparam = {}
  if params is None:
    params = []

  def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      try:
        rs = func(*args, **kwargs)
        return rs
      except exceptions as ex:
        return ex.message if not f_return else f_return(*params, **kwparam)
    return wrapper

  if _func is None:
    return decorator
  else:
    return decorator(_func)


# def xml_return(_func=None, *, encoder_cls=None):
#
#   def decorator(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#       rs = func(*args, **kwargs)
#       return json.dumps(rs, cls=PiJsonEncoder if not encoder_cls else encoder_cls)
#
#     return wrapper
#
#   if _func is None:
#     return decorator
#   else:
#     return decorator(_func)