import pystac


PROVIDERS = [
    pystac.Provider(name='Atlantic',
                    roles=['producer'],
                    url='https://atlantic.tech/'),
    pystac.Provider(name='Preston\'s MacBook',
                    roles=['host'],
                    url='https://mysite.com/')
]