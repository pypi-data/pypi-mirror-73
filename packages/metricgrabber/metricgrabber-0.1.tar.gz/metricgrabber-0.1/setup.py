import setuptools

setuptools.setup(
    name='metricgrabber',
    version='0.1',
    author='Gallardo994',
    author_email='evolutionv8@yandex.ru',
    url='https://github.com/Gallardo994/metricgrabber',
    description='Metricgrabber - Python Prometheus Exporter',
    install_requires=['flask', 'kthread'],
    packages=setuptools.find_packages(),
    license='GPL V3',
    long_description='Git: https://github.com/Gallardo994/metricgrabber',
)