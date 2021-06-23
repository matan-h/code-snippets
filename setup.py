from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("code_snippets\\version.py","r") as sn:
    version = sn.readlines()[0].split("=")[1].strip()[1:][:-1]

setup(
    name='code_snippets',

    version='0.0.0',
    license='MIT',
    description='',
    author='matan h',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email='matan.honig2@gmail.com',
    url='https://github.com/matan-h/code_snippets',
    packages=['code_snippets'],
    entry_points={
            "console_scripts": [
                "snippets = code_snippets.__main__:main",
                # "info = mpconvert.info:cli",
            ]
        },
    install_requires=['howdoi','PySimpleGUI', 'outdated'],

    # python_requires = '',

)
