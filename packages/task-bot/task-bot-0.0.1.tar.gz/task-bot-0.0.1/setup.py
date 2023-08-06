"""
setup
"""
import os
import setuptools


def get_version() -> str:
    """
    read version from VERSION file
    """
    version = '0.0.0'

    with open(
            os.path.join(
                os.path.dirname(__file__),
                'VERSION'
            )
    ) as version_fh:
        # Get X.Y.Z
        version = version_fh.read().strip()

    return version


def get_long_description() -> str:
    """get long_description"""
    with open('README.md', 'r') as readme_fh:
        return readme_fh.read()


def get_install_requires() -> str:
    """get install_requires"""
    with open('requirements.txt', 'r') as requirements_fh:
        return requirements_fh.read().splitlines()


setuptools.setup(
    name='task-bot',
    version=get_version(),
    author='wj-Mcat',
    author_email='1435130236@qq.com',
    description='task-bot is designed for simple&strong task-oriented dialogue bot',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    license='Apache-2.0',
    url='https://github.com/wj-Mcat/task-bot',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    install_requires=get_install_requires(),
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
)
