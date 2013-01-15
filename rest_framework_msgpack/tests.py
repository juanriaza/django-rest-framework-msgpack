import decimal
import datetime
from StringIO import StringIO
from django.test import TestCase
from rest_framework_msgpack.renderers import MessagePackRenderer
from rest_framework_msgpack.parsers import MessagePackParser


class MessagePackRendererTests(TestCase):
    """
    Tests specific to the MessagePack Renderer
    """

    def test_render(self):
        """
        Test basic MessagePack rendering.
        """
        obj = {'foo': ['bar', 'baz']}
        renderer = MessagePackRenderer()
        content = renderer.render(obj, 'application/msgpack')
        msgpack_repr = '\x81\xa3foo\x92\xa3bar\xa3baz'
        self.assertEquals(content, msgpack_repr)

    def test_render_and_parse(self):
        """
        Test rendering and then parsing returns the original object.
        IE obj -> render -> parse -> obj.
        """
        obj = {'foo': ['bar', {'baz': [1, 2]}]}

        renderer = MessagePackRenderer()
        parser = MessagePackParser()

        content = renderer.render(obj, 'application/msgpack')
        data = parser.parse(StringIO(content))
        self.assertEquals(obj, data)

    def test_datetime(self):
        obj = {'my_datetime': datetime.datetime.now()}

        renderer = MessagePackRenderer()
        parser = MessagePackParser()

        content = renderer.render(obj, 'application/msgpack')
        data = parser.parse(StringIO(content))
        self.assertEquals(obj, data)

    def test_date(self):
        obj = {'my_date': datetime.date.today()}

        renderer = MessagePackRenderer()
        parser = MessagePackParser()

        content = renderer.render(obj, 'application/msgpack')
        data = parser.parse(StringIO(content))
        self.assertEquals(obj, data)

    def test_time(self):
        obj = {'my_date': datetime.datetime.now().time()}

        renderer = MessagePackRenderer()
        parser = MessagePackParser()

        content = renderer.render(obj, 'application/msgpack')
        data = parser.parse(StringIO(content))
        self.assertEquals(obj, data)

    def test_decimal(self):
        obj = {'my_date': decimal.Decimal(1) / decimal.Decimal(7)}

        renderer = MessagePackRenderer()
        parser = MessagePackParser()

        content = renderer.render(obj, 'application/msgpack')
        data = parser.parse(StringIO(content))
        self.assertEquals(obj, data)
