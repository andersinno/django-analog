import setuptools

dev_deps = ['pytest', 'pytest-django', 'pytest-cov', 'pep257', 'flake8']

if __name__ == '__main__':
    setuptools.setup(
        name='django-analog',
        version='0.2.0',
        url='https://github.com/andersinno/django-analog',
        author='Anders Innovations',
        license='MIT',
        install_requires=[
            'Django',
            'jsonfield>=1.0,<1.1'
        ],
        tests_require=dev_deps,
        extras_require={"dev": dev_deps},
        packages=setuptools.find_packages('.', exclude=('analog_tests',)),
        include_package_data=True,
    )
