from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    description = f.read()
setup(
    name='graphical-formula',
    version='0.0.2',
    py_modules=['graphical'],
    license='LICENSE',
    author='17097231932',
    author_email='17097231932@163.com',
    url='https://17097231932.github.io/graphical/',
    description='快速的创建和使用图形公式',
    long_description=description
)
