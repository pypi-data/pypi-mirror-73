from os import path
from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    app=['__main__.py'],
    name='flopferret',
    version='0.1.4',
    description='A Texas Hold\'em board texture analyzer',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/JulianAndrews/pyeval7',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Games/Entertainment',
    ],
    keywords='poker equity',
    packages=['flopferret'],
    entry_points={
        'gui_scripts': ['flopferret=flopferret:main']
    },
    install_requires=['pyxdg', 'eval7>=0.1.6', 'PyQt5'],
    options={'py2app': {
        'iconfile': 'macos/flopferret.icns',
        'packages': 'PyQt5,eval7',
    }},
)
