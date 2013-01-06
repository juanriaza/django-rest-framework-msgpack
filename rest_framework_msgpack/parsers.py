import decimal
import msgpack
from dateutil.parser import parse

from rest_framework.parsers import BaseParser
from rest_framework.exceptions import ParseError


class MessagePackDecoder(object):

    def decode(self, obj):
        if '__class__' in obj:
            decode_func = getattr(self, 'decode_%s' % obj['__class__'])
            return decode_func(obj)
        return obj

    def decode_datetime(self, obj):
        return parse(obj['as_str'])

    def decode_date(self, obj):
        return parse(obj['as_str']).date()

    def decode_time(self, obj):
        return parse(obj['as_str']).time()

    def decode_decimal(self, obj):
        return decimal.Decimal(obj['as_str'])


class MessagePackParser(BaseParser):
    """
    Parses MessagePack-serialized data.
    """

    media_type = 'application/msgpack'

    def parse(self, stream, media_type=None, parser_context=None):
        try:
            return msgpack.unpackb(stream,
                use_list=True,
                object_hook=MessagePackDecoder().decode)
        except Exception, exc:
            raise ParseError('MessagePack parse error - %s' % unicode(exc))
