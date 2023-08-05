from setuptools import setup, find_packages

setup(
    name='bhav',
    version='1.0.9',
    author="Ajay Sharma",
    author_email="deal.ajay@gmail.com",
    python_requires='>=3',
    packages=find_packages(),
    include_package_data=True,
    url="https://gitlab.com/sw8fbar/bhav",
    description="CLI to download End of day Stock data from BSE and NSE",
    long_description=open("README.md").read(),
    license="LICENSE.txt",
    install_requires=[
        'Click',
        'requests',
        'python-dotenv',
        'PyInquirer',
        'flask',
        'pandas',
        'marshmallow',
        'flask_cors'
    ],
    entry_points={
        'console_scripts': [
            'bhav=bhav.main:cli',
        ]
    },
)