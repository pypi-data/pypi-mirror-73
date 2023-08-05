from django.conf import settings


class Settings(object):
    """
    Module settings helper.
    """
    prefix = 'CDN_'

    @staticmethod
    def get(key, default=None, default_setting=None):
        key = '{}{}'.format(Settings.prefix, key)
        if not hasattr(settings, key):
            return default if default_setting is None else getattr(settings, default_setting)

        return getattr(settings, key)
