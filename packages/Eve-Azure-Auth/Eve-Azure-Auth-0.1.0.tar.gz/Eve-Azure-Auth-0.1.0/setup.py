from setuptools import setup


def get_info(info):
    for line in open('src/__version__.py').readlines():
        if line.startswith(info):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]

    raise RuntimeError('Unable to find version string.')


with open('README.md', 'r') as f:
    readme = f.read()

reqs = [
    'cachecontrol<1',
    'cryptography<3',
    'PyJWT<2',
    'eve<2',
]

setup(
    name=get_info('__title__'),
    version=get_info('__version__'),
    description=get_info('__description__'),
    long_description=readme,
    long_description_content_type='text/markdown',
    author=get_info('__author__'),
    author_email=get_info('__author_email__'),
    url=get_info('__url__'),
    install_requires=reqs,
    zip_safe=False,
    include_package_data=True,
    exclude_package_data={'': ['README.md']},
    package_dir={'eve_azure_ad_auth': 'src'},
    packages=['eve_azure_ad_auth'],
)
