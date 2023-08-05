import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="play_store_scrapper",
    version="1.0.2",
    author="Muhammad Tayyab Sheikh",
    author_email="cstayyab@gmail.com",
    description="A python package to scrape data from Google Play Store using Selenium",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cstayyab/play-store-scrapper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'selenium',
        'htmlparser',
        'requests'
    ]
)