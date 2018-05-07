from setuptools import setup

setup(
    name='serokellwarrior',
    packages=['serokellwarrior'],
    entry_points={
        'console_scripts': [
            'serokellwarrior-export=serokellwarrior.export:main',
            'serokellwarrior-hook=serokellwarrior.hook:main',
            'serokellwarrior-report=serokellwarrior.report:main',
        ],
    },
    install_requires=['bugwarrior']
)
