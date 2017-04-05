import setuptools

dev_deps = [
    'autopep8',
    'flake8',
    'isort',
    'pep257',
    'pytest-cov',
    'pytest-django>=3.0.0',
    'pytest>=3.0.0',
]

if __name__ == '__main__':
    setuptools.setup(
        name='django-analog',
        version='0.4.0',
        url='https://github.com/andersinno/django-analog',
        author='Anders Innovations',
        license='MIT',
        install_requires=['Django'],
        tests_require=dev_deps,
        extras_require={"dev": dev_deps},
        packages=setuptools.find_packages('.', exclude=('analog_tests',)),
        include_package_data=True,
    )
