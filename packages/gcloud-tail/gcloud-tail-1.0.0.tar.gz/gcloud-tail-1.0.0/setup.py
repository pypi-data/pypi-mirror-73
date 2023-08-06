from setuptools import setup

setup(
    name='gcloud-tail',
    version='1.0.0',
    classifiers = [
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: System :: Logging',
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    py_modules=['gcloudtail'],
    entry_points={
        'console_scripts': [
            'gcloud-tail = gcloudtail:main',
        ],
    },
)
