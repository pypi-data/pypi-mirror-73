from setuptools import setup

setup(
    name='mdi',
    version='1.0',

    description='Download pictures and videos from Instagram',
    long_description="visit https://python.org",
    url='https://in.future',

    author='Mazidul islam',
    author_email='immazidulislam@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Programming Language :: Python',
    ],

    keywords='instagram-scraper instagram-feed downloader videos photos pictures instagram-photos instagram-downloader',

    packages=["mdi"],
    install_requires=['mdn'],
    entry_points={
        'console_scripts': [
            'mdi=mdi:main',
        ],
    },

)
