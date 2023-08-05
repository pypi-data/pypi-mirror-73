from setuptools import setup, find_packages

setup(
    name='ravenml',
    version='1.1',
    description='ML Training CLI Tool',
    license='MIT',
    packages=find_packages(),
    author='Carson Schubert, Abhi Dhir, Pratyush Singh',
    author_email='carson.schubert14@gmail.com',
    keywords= ['machine learning', 'data science'],
    download_url = 'https://github.com/autognc/ravenML/archive/v1.1.tar.gz',
    install_requires=[
        'Click>=7.0',
        'click-plugins>=1.0.4',
        'questionary>=1.0.2',
        'boto3>=1.9.86', 
        'shortuuid>=0.5.0',
        'halo>=0.0.26'
        'colorama>=0.3.9',
        'pyaml>=19.4.1',
    ],
    tests_require=[
        'pytest',
        'moto'
    ],
    entry_points='''
      [console_scripts]
      ravenml=ravenml.cli:cli
    ''',
)
      