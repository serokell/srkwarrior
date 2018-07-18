from setuptools import setup

setup(
    name='srkwarrior',
    packages=['srkwarrior'],
    entry_points={
        'console_scripts': [
            'srkwarrior-export=srkwarrior.export:main',
            'srkwarrior-hook=srkwarrior.hook:main',
            'srkwarrior-report=srkwarrior.report:main',
        ],
    },
    install_requires=['bugwarrior']
)
