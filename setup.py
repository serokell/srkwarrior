from setuptools import setup

setup(
    name='srkwarrior',
    packages=['srkwarrior'],
    entry_points={
        'console_scripts': [
            'srkwarrior-export=srkwarrior.export:main',
            'srkwarrior-hook=srkwarrior.hook:main',
        ],
    },
    install_requires=['bugwarrior']
)
