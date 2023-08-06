from setuptools import setup, find_namespace_packages

setup(
    name="django-cassandra-common",
    version="0.0.2",
    author="Didier Gaona",
    author_email="didiergaona@gmail.com",
    install_requires=["Django>=3.0.6", 'djangorestframework>=3.11.0', 'cassandra-driver>=3.23.0', 'requests>=2.23.0',
                      'django-filter>=2.3.0', 'setuptools>=46.4.0', 'django-cassandra-engine>=1.6.1',
                      'drf-yasg>=1.17.1'],
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    url='https://github.com/didier47/django-cassandra-common',
    description='Common classes I have found useful to develop with Django and Cassandra',
    license='GNU General Public License v3.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    download_url='https://github.com/didier47/django-cassandra-common/archive/0.0.1.tar.gz'
)
