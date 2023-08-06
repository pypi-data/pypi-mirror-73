# ==================================================================
#       文 件 名: fields.py
#       概    要: Fields
#       作    者: IT小强 
#       创建时间: 6/18/20 3:54 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

import json

from django.core.exceptions import ValidationError
from django.db.models import Field, TextField
from django.utils.translation import gettext_lazy as _

from .forms import JSONFormField, EditorMdFormField
from .helper import get_kelove_databases_settings, json_value_to_python


class JSONField(Field):
    """
    JSON 编辑器字段
    """

    empty_strings_allowed = False

    description = _("JSON 编辑器字段")

    default_error_messages = {
        'json_decode_error': _('JSON转码失败'),
        'invalid': _('“%(value)s”的类型只能为dict、list、tuple、set、json字符串。'),
        'invalid_nullable': _('“%(value)s”的类型只能为dict、list、tuple、set、json字符串或者None。'),
    }

    def __init__(self, *args, **kwargs):
        kwargs['field_settings'] = kwargs.get('field_settings', {})
        self._field_settings = {**get_kelove_databases_settings('JSON_FIELD_SETTINGS', {}), **kwargs['field_settings']}
        kwargs.pop('field_settings')
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return "TextField"

    def formfield(self, **kwargs):
        kwargs['form_class'] = JSONFormField
        kwargs['field_settings'] = self._field_settings
        return super().formfield(**kwargs)

    def to_python(self, value):

        if self.null and value in [None, '']:
            return None

        if value in self.empty_values:
            return {}

        try:
            return json_value_to_python(value)
        except json.JSONDecodeError:
            raise ValidationError(
                self.error_messages['json_decode_error'],
                code='invalid',
                params={'value': value},
            )
        except ValueError:
            raise ValidationError(
                self.error_messages['invalid_nullable' if self.null else 'invalid'],
                code='invalid',
                params={'value': value},
            )

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value is None:
            return None
        return json.dumps(self.to_python(value))

    def value_from_object(self, obj):
        return self.to_python(super().value_from_object(obj))


class EditorMdField(TextField):
    """
    Markdown 编辑器字段
    """
    description = _("Markdown 编辑器字段")

    def __init__(self, *args, **kwargs):
        kwargs['field_settings'] = kwargs.get('field_settings', {})
        self._field_settings = {
            **get_kelove_databases_settings('EDITOR_MD_FIELD_SETTINGS', {}),
            **kwargs['field_settings']
        }
        kwargs.pop('field_settings')
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['form_class'] = EditorMdFormField
        kwargs['field_settings'] = self._field_settings
        return super().formfield(**kwargs)
