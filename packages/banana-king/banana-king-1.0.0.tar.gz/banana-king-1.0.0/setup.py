from setuptools import setup, find_packages

setup(
    name='banana-king',
    version='1.0.0',
    description=('Banana King Nerver Absent! Timed execution.'),
    long_description=open('README.rst').read(),
    author='twfb',
    author_email='twfb@hotmail.com',
    maintainer='twfb',
    maintainer_email='twfb@hotmail.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    include_package_data=True,
    url='https://github.com/dhgdhg/Banana-King',
    classifiers=[
        'Development Status :: 4 - Beta', 'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
    entry_points={
        'console_scripts': ['banana-king=__init__.__init__:main'],
    })
