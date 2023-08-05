from setuptools import setup

version = '0.2.6'

setup(
    name='jupyterhub-keystoneauthenticator',
    version=version,
    description='Keystone Authenticator for JupyterHub',
    url='https://github.com/chameleoncloud/keystoneauthenticator',
    author='Jason Anderson',
    author_email='jasonanderson@uchicago.edu',
    license='3 Clause BSD',
    packages=['keystoneauthenticator'],
    install_requires=[
        'jupyterhub',
        'keystoneauth1',
        'tornado',
        'traitlets',
    ],
    entry_points={
        'jupyterhub.authenticators': [
            'keystone = keystoneauthenticator:KeystoneAuthenticator',
        ],
    },
)
