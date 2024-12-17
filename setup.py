from setuptools import setup, find_packages

setup(
    name='trading_bot',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'yfinance',
        'pandas',
        'oandapyV20',
        'apscheduler',
    ],
    entry_points={
        'console_scripts': [
            'trading-bot=trading_bot.main:main',
        ],
    },
)
