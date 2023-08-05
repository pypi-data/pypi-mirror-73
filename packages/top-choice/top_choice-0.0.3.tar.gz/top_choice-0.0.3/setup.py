import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="top_choice",
    version="0.0.3",
    author="Brian Willett",
    author_email="bmwillett1@gmail.com",
    description="A package using topological data analysis to achieve robust product recommendations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bmwillett/topological-recommendations",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
    'numpy==1.17.2',
    'pandas==0.25.1',
    'matplotlib==3.1.1',
    'scipy==1.4.1',
    'Keras==2.3.1',
    'tensorflow==2.2.0',
    'scikit_learn>=0.21.3',
    'predictor==0.1.2',
    'adversary==1.1.1',
    'pymapper==0.1.0',
    ]
)
