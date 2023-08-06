from setuptools import setup


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="Ola-Bino-Gaussian-Distributions",
    version="1.0.5",
    description="A Python package to get Binomial and Gaussian Distributions Package.",
    author="Ajayi Olabode O",
    author_email="boraton2010@gmail.com",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/boratonAJ/Ola-BGaussian-Distributions",
    license="MIT",
    keywords="Binomial Gaussian Distribution Probability Histogram BarChart",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
     ],
    zip_safe=False,
    include_package_data=True,
    packages=["Ola-Bino-Gaussian-Distributions"]
)
