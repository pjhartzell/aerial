from pystac import Provider, ProviderRole


PROVIDERS = [
    Provider(name='Atlantic',
                  roles=[ProviderRole.PRODUCER],
                  url='https://atlantic.tech/'),
    Provider(name='Preston\'s MacBook',
                  roles=[ProviderRole.HOST],
                  url='https://mysite.com/')
]
