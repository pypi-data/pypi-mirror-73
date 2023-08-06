import setuptools

with open("README.md", "r",encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="senti_c", 
    version="0.0.4",
    keywords='sentiment analysis toolkit',
    author="Julie Tu",
    author_email="flywinglan@gmail.com",
    description="A sentiment analysis package used for traditional Chinese.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/julielanblue/senti_c",
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        'Topic :: Software Development :: Build Tools',
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.7',
    install_requires=[
		'opencc==1.1.1',
        'numpy==1.18.5',
        'torch==1.5.0',
        'transformers==2.11.0',
        'pandas==1.0.4',
        'scikit-learn==0.23.1',
		'tensorflow==2.2.0',
    ],
)