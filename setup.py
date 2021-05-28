from setuptools import setup

setup(
    name = 'nyanMigen',
    scripts = [
        'nyanMigen.py'
    ],
    install_requires = ["pprintast", "astunparse"]
)
