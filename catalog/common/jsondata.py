import copy
from datetime import date, datetime
from importlib import import_module

import django
from django.conf import settings
from django.core.exceptions import FieldError
from django.db.models import fields
from django.utils import dateparse, timezone

from functools import partialmethod
from django.db.models import JSONField


__all__ = ('BooleanField', 'CharField', 'DateField', 'DateTimeField', 'DecimalField', 'EmailField', 'FloatField', 'IntegerField', 'IPAddressField', 'GenericIPAddressField', 'NullBooleanField', 'TextField', 'TimeField', 'URLField', 'ArrayField')


class JSONFieldDescriptor(object):
    def __init__(self, field):
        self.field = field

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        json_value = getattr(instance, self.field.json_field_name)
        if isinstance(json_value, dict):
            if self.field.attname in json_value or not self.field.has_default():
                value = json_value.get(self.field.attname, None)
                if hasattr(self.field, 'from_json'):
                    value = self.field.from_json(value)
                return value
            else:
                default = self.field.get_default()
                if hasattr(self.field, 'to_json'):
                    json_value[self.field.attname] = self.field.to_json(default)
                else:
                    json_value[self.field.attname] = default
                return default
        return None

    def __set__(self, instance, value):
        json_value = getattr(instance, self.field.json_field_name)
        if json_value:
            assert isinstance(json_value, dict)
        else:
            json_value = {}

        if hasattr(self.field, 'to_json'):
            value = self.field.to_json(value)

        if not value and self.field.blank and not self.field.null:
            try:
                del json_value[self.field.attname]
            except KeyError:
                pass
        else:
            json_value[self.field.attname] = value

        setattr(instance, self.field.json_field_name, json_value)


class JSONFieldMixin(object):
    """
    Override django.db.model.fields.Field.contribute_to_class
    to make a field always private, and register custom access descriptor
    """

    def __init__(self, *args, **kwargs):
        self.json_field_name = kwargs.pop('json_field_name', 'metadata')
        super(JSONFieldMixin, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, private_only=False):
        self.set_attributes_from_name(name)
        self.model = cls
        self.concrete = False
        self.column = self.json_field_name
        cls._meta.add_field(self, private=True)

        if not getattr(cls, self.attname, None):
            descriptor = JSONFieldDescriptor(self)
            setattr(cls, self.attname, descriptor)

        if self.choices is not None:
            setattr(cls, 'get_%s_display' % self.name,
                    partialmethod(cls._get_FIELD_display, field=self))

    def get_lookup(self, lookup_name):
        # Always return None, to make get_transform been called
        return None

    def get_transform(self, name):
        class TransformFactoryWrapper:
            def __init__(self, json_field, transform, original_lookup):
                self.json_field = json_field
                self.transform = transform
                self.original_lookup = original_lookup

            def __call__(self, lhs, **kwargs):
                lhs = copy.copy(lhs)
                lhs.target = self.json_field
                lhs.output_field = self.json_field
                transform = self.transform(lhs, **kwargs)
                transform._original_get_lookup = transform.get_lookup
                transform.get_lookup = lambda name: transform._original_get_lookup(self.original_lookup)
                return transform

        json_field = self.model._meta.get_field(self.json_field_name)
        transform = json_field.get_transform(self.name)
        if transform is None:
            raise FieldError(
                "JSONField '%s' has no support for key '%s' %s lookup" %
                (self.json_field_name, self.name, name)
            )

        return TransformFactoryWrapper(json_field, transform, name)


class BooleanField(JSONFieldMixin, fields.BooleanField):
    def __init__(self, *args, **kwargs):
        super(BooleanField, self).__init__(*args, **kwargs)
        if django.VERSION < (2, ):
            self.blank = False


class CharField(JSONFieldMixin, fields.CharField):
    pass


class DateField(JSONFieldMixin, fields.DateField):
    def to_json(self, value):
        if value:
            assert isinstance(value, (datetime, date))
            return value.strftime('%Y-%m-%d')

    def from_json(self, value):
        if value is not None:
            return dateparse.parse_date(value)


class DateTimeField(JSONFieldMixin, fields.DateTimeField):
    def to_json(self, value):
        if value:
            if not timezone.is_aware(value):
                value = timezone.make_aware(value)
            return value.isoformat()

    def from_json(self, value):
        if value:
            return dateparse.parse_datetime(value)


class DecimalField(JSONFieldMixin, fields.DecimalField):
    pass


class EmailField(JSONFieldMixin, fields.EmailField):
    pass


class FloatField(JSONFieldMixin, fields.FloatField):
    pass


class IntegerField(JSONFieldMixin, fields.IntegerField):
    pass


class IPAddressField(JSONFieldMixin, fields.IPAddressField):
    pass


class GenericIPAddressField(JSONFieldMixin, fields.GenericIPAddressField):
    pass


class NullBooleanField(JSONFieldMixin, fields.NullBooleanField):
    pass


class TextField(JSONFieldMixin, fields.TextField):
    pass


class TimeField(JSONFieldMixin, fields.TimeField):
    def to_json(self, value):
        if value:
            if not timezone.is_aware(value):
                value = timezone.make_aware(value)
            return value.isoformat()

    def from_json(self, value):
        if value:
            return dateparse.parse_time(value)


class URLField(JSONFieldMixin, fields.URLField):
    pass


class ArrayField(JSONFieldMixin, JSONField):
    pass
