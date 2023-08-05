import setuptools
import urllib.request


DESCRIPTION = 'A standardized collection of python libs and tools'

try:
    with open('README.md', 'r') as f:
        LONG_DESCRIPTION = f.read()
except FileNotFoundError:
    LONG_DESCRIPTION = DESCRIPTION

try:
    with open('VERSION', 'r') as f:
        VERSION = f.read()
except FileNotFoundError:
    VERSION = 'test'

# To whenever PYPI allows direct references for dependencies
# deps = [
#     {
#         'name': 'aiocheck',
#         'url': 'https://github.com/kruserr/aiocheck',
#         'tag': '',
#     },
# ]

# for i in range(len(deps)):
#     try:
#         if (deps[i]['tag'] is None) or (len(deps[i]['tag']) == 0):
#             raise KeyError()
#     except KeyError:
#         request = urllib.request.urlopen(f"{deps[i]['url']}/releases/latest").geturl()
#         deps[i]['tag'] = request.split('/')[::-1][0]
    
#     deps[i] = f"{deps[i]['name']} @ git+{deps[i]['url']}@{deps[i]['tag']}"

setuptools.setup(
    name='i6',
    version=VERSION,
    author='kruserr',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/kruserr/i6',
    keywords='i6 toolchain collection libs tools',
    project_urls={
        'Documentation': 'https://github.com/kruserr/i6/wiki',
        'Source': 'https://github.com/kruserr/i6',
    },
    packages=setuptools.find_packages(
        where='src',
        exclude=['tests*'],
    ),
    package_dir={
        '': 'src',
    },
    install_requires=[
        'docker',
        'pyftpdlib',
        'SQLAlchemy',
        'marshmallow',
    ],
    entry_points = {
        'console_scripts': ['i6=i6.__main__:main'],
    },
    zip_safe=True,
    classifiers=[
        'Topic :: Software Development',
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
