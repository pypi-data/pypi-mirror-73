import setuptools

with open('./README.md', 'r') as f:
  long_description = f.read()

setuptools.setup(
    name='beamx',
    version='0.0.1',
    author='Arata Furukawa',
    author_email='old.river.new@gmail.com',
    description='A small example package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/pypa/sampleproject',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'apache-beam>=2.22.0',
        'boto3>=1.14.15',
        'pyorc>=0.3.0',
    ],
    python_requires='>=3.6',
    test_suite='pytest',
)
