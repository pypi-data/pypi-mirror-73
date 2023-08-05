from setuptools import setup, find_packages


setup(name='colorthistext',
        version='0.1',
        url='https://gitlab.com/kelvium/colorthistext',
        license='MIT',
        author='Kelvium',
        author_email='contact@kelvium.design',
        description='Lib to color text.',
        packages=find_packages(exclude=['tests']),
        long_description=open('README.rst').read(),
        zip_safe=False)

