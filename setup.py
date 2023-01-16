from setuptools import setup, find_namespace_packages

__version__ = '0.0.1'

setup(
    name='edgio-console-app',
    description='Edgio Console',
    version=__version__,

    license='For LLNW internal usage ONLY',
    author='Core QA Automation Team',
    author_email='mbondarenko@llnw.com',

    python_requires='>=3.8.7',

    packages=find_namespace_packages(include=['ltf2.console_app.*']),

    install_requires=[
        'pytest',
        'allure-pytest',
        'pytest-playwright',
        'ltf2-util',
    ],
)
