from .core.factory import Factory


def client(client, **kwargs):
    instance = Factory(
        'Client',
        f'zdk.zinobe.{client}.client'
    ).get_instance()
    return instance
