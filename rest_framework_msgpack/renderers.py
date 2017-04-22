import msgpack
import decimal
import datetime

from rest_framework.renderers import BaseRenderer


class MessagePackEncoder(object):

    def encode(self, obj):
        if isinstance(obj, datetime.datetime):
            return {'__class__': 'datetime', 'as_str': obj.isoformat()}
        elif isinstance(obj, datetime.date):
            return {'__class__': 'date', 'as_str': obj.isoformat()}
        elif isinstance(obj, datetime.time):
            return {'__class__': 'time', 'as_str': obj.isoformat()}
        elif isinstance(obj, decimal.Decimal):
            return {'__class__': 'decimal', 'as_str': str(obj)}
        else:
            return obj


class MessagePackRenderer(BaseRenderer):
    """
    Renderer which serializes to MessagePack.
    """

    media_type = 'application/msgpack'
    format = 'msgpack'
    render_style = 'binary'
    charset = None

    def render(self, data, media_type=None, renderer_context=None):
        """
        Renders *obj* into serialized MessagePack.
        """
        if data is None:
            return ''
        return msgpack.packb(data, default=MessagePackEncoder().encode)
