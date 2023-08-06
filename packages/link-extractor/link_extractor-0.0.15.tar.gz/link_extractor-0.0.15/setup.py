import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="link_extractor",
    version="0.0.15",
    author="Yunzhi Gao",
    author_email="gaoyunzhi@gmail.com",
    description="Extract Links from news source, ranked by importance.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gaoyunzhi/link_extractor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'bs4',
        'telegram_util>=0.0.27',
        'cached_url>=0.0.1',
    ],
    python_requires='>=3.0',
)