from setuptools import setup

setup(
    name='test_ess_software',
    version='1.0',
    description='Ess test software which requires api & test set folder to give visual representation of testing automation',
    author='ayush panwar',
    author_email='ayushpanwar691@gmail.com',
    license='MIT',
    packages=['test'],
    install_requires=[
        'tk',
        'customtkinter'
    ]
)