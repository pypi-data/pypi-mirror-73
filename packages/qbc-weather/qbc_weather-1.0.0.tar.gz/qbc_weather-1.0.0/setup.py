#!/user/bin/env python

from distutils.core import setup

setup(
    name='qbc_weather',
    version='1.0.0',
    description='Get The Weather App',
    long_description='Get the weather forecast for the next 15 days',
    author='Charles',
    author_email = 'charles@shinelab.cn',
    keywords=['pip3', 'weather', 'weathers','python3','python','weather forecast'],
    url='https://www.shinelab.cn/',
    packages=['qbc_weather'],
    packages_data={'qbc_weather': ['*.py']},
    license='MIT',
    install_requires=['requests', 'ybc_config', 'ybc_exception']
)
