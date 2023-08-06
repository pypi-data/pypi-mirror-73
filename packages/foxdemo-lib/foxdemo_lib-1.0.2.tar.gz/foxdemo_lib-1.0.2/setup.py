from setuptools import setup, find_packages

setup(
    name='foxdemo_lib',
    version='1.0.2',
    author='fiebiga',
    author_email='fiebig.adam@gmail.com',
    description='Common lib for microservice anatomy',
    packages=find_packages(),
    install_requires=["flask", "flask-restful"],
)