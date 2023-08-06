import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = ['pymysql', 'sqlalchemy']

test_requirements = ['pytest', 'pytest-cov', 'pytest-watch', 'pytest-reportlog']

setuptools.setup(
    author="SALT Software Engineers",
    author_email="salt-support@salt.ac.za",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    description="A tool for retreiving and unpacking stored ELS data.",
    install_requires=requirements,
    license="MIT license",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="salt_cellar",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    test_suite='tests',
    tests_require=test_requirements,
    url="https://bitbucket.org/saao/salt_cellar",
    version="0.1.1",
)
