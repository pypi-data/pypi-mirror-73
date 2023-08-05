import os
from setuptools import setup, find_packages


# Get the README.md text
with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as f:
    readme = f.read()

# Parse ftrack_query.py for a version
with open(os.path.join(os.path.dirname(__file__), 'ftrack_query.py'), 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = eval(line.split('=')[1].strip())
            break
    else:
        raise RuntimeError('no version found')

# Get the pip requirements
with open(os.path.join(os.path.dirname(__file__), 'requirements.txt'), 'r') as f:
    requirements = [line.strip() for line in f]

setup(
    name = 'ftrack-query',
    packages = find_packages(),
    version = version,
    license='MIT',
    description = 'Easy query generation for the FTrack API.',
    long_description=readme,
    long_description_content_type='text/markdown',
    author = 'Peter Hunt',
    author_email='peter@huntfx.uk',
    py_modules=['ftrack_query'],
    url = 'https://github.com/Peter92/ftrack-query',
    download_url = 'https://github.com/Peter92/ftrack-query/archive/{}.tar.gz'.format(version),
    project_urls={
        'Documentation': 'https://github.com/Peter92/ftrack-query/wiki',
        'Source': 'https://github.com/Peter92/ftrack-query',
        'Issues': 'https://github.com/Peter92/ftrack-query/issues',
    },
    keywords = ['ftrack', 'api', 'query'],
    install_requires=requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    python_requires=('>=2.7.9, <3.0')
)
