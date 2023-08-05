from setuptools import setup, find_packages

setup(
    name='almadenkorea',
    version='0.0.3',   #20200703
    description='almaden package',
    author='tajinbae',
    author_email='bjin86@gmail.com',
    url='https://github.com/BaeJin/almadenkorea',
    download_url='https://github.com/BaeJin/almadenkorea/archive/master.zip',
    install_requires=['pandas','pymysql'],
    packages=find_packages(exclude=[]),
    keywords=['sql'],
    python_requires='>=3',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)