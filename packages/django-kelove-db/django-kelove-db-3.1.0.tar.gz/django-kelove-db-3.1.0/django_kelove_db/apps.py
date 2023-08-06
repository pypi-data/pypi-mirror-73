# ==================================================================
#       文 件 名: apps.py
#       概    要: DjangoKeloveDbConfig
#       作    者: IT小强
#       创建时间: 6/9/20 5:57 PM
#       修改时间:
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjangoKeloveDbConfig(AppConfig):
    label = 'django_kelove_db'
    name = 'django_kelove_db'
    verbose_name = _('Django Db 增强')
