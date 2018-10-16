from setuptools import setup, find_packages

setup(
    name='HTML-as-programming-language',
    version='0.1.9',
    author="hilkojj",
    author_email="hilkojj@outlook.com",
    url="https://github.com/HTML-as-programming-language/HTML-as-programming-language",
    description='(WIP) Write HTML-code that compiles to C',
    long_description=open('README.txt').read(),
    packages=find_packages(),
    install_requires=[
        "colorama",      # used to print with colors
        "pyavrutils"
    ],
    entry_points={
        'console_scripts': [
            'htmlclangsvr = htmlc.lang_server:main',
            'htmlc = htmlc.compiler:main'
        ]
    }
)
