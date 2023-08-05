from setuptools import setup, find_packages
import io

with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='zyzhi',
    license='Apache License 2.0',
    version='0.2.1',
    maintainer='Yuanzhen Zhou',
    maintainer_email='szrednick@gmail.com',
    packages=find_packages(include=['zyzhi', 'zyzhi.*']),
    zip_safe=False,
    include_package_data=True,
    url='https://github.com/zhouyuanzhen/pypi-helloworld',
    author='Yuanzhen Zhou',
    author_email='szrednick@gmail.com',
    description='A sample PyPI helloworld project',
    long_description=readme,
    install_requires=[],
        extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    },
)
