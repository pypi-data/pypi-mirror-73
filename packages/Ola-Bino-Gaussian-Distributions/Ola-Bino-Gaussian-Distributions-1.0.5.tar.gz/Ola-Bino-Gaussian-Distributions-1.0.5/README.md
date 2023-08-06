# Example Package

This package provides the Gaussian distribution and Binomial distribution classes.

Gaussian:
=========

Gaussian distribution class for calculating and visualizing a Gaussian distribution. Attributes: mean (float) - representing the mean value of the distribution. stdev (float) - representing the standard deviation of the distribution. data_list (list of floats) - a list of floats extracted from the data file.

## Methods:

   *  calculate_mean() - Function to calculate the mean of the data set.

   * calculate_stdev() - Function to calculate the standard deviation of the data set.

   *  plot_histogram() - Function to output a histogram of the instance variable data using matplotlib pyplot library.

   *  read_data_file(filename) - Function to read in data from a txt file. The txt file should have one number (float) per line. The numbers       are stored in the data attribute.

   *  pdf(x) - Probability density function calculator for the gaussian distribution Args: x (float): point for calculating the probability         density function Returns: float: probability density function output.

   *  plot_histogram_pdf(n_spaces = 50) - Function to plot the normalized histogram of the data and a plot of the probability density               function along the same range Args: n_spaces (int): number of data points Returns: list: x values for the pdf plot list: y values for         the pdf plot.

   *  add(other) - Function to add together two Gaussian distributions Args: other (Gaussian): Gaussian instance Returns: Gaussian: Gaussian       distribution

   *  repr() - Function to output the characteristics of the Gaussian instance


Binomial:
=========

Binomial distribution class for calculating and visualizing a Binomial distribution. Attributes: mean (float) representing the mean value of the distribution stdev (float) representing the standard deviation of the distribution data_list (list of floats) a list of floats to be extracted from the data file p (float) representing the probability of an event occurring n (int) number of trials


## Methods:

   *  calculate_mean() - Function to calculate the mean from p and n

   *  calculate_stdev() - Function to calculate the standard deviation from p and n.

   *  read_data_file(filename) - Function to read in data from a txt file. The txt file should have one number (float) per line. The numbers       are stored in the data attribute.

   *  replace_stats_with_data() - Function to calculate p and n from the data set Args: None Returns: float: the p value float: the n value

   *  plot_bar() - Function to output a histogram of the instance variable data using matplotlib pyplot library.

   *  pdf(k) - Probability density function calculator for the gaussian distribution. Args: x (float): point for calculating the probability       density function Returns: float: probability density function output

   *  plot_bar_pdf() - Function to plot the pdf of the binomial distribution Args: None Returns: list: x values for the pdf plot list: y           values for the pdf plot

   *  add(other) - Function to add together two Binomial distributions with equal p Args: other (Binomial): Binomial instance Returns:             Binomial: Binomial distribution

   *  repr() - Function to output the characteristics of the Binomial instance.


Files:
======

* Generaldistribution.py - contains Distribution class, its attributes and methods being inherited by Gaussian and Binomial class.
* Gaussiandistribution.py - contains Gaussian class, its attributes and methods stated above in Ola-Bino-Gaussian-Distributions package summary.
* Binomialdistribution.py - contains Binomial class, its attributes and methods stated above in Ola-Bino-Gaussian-Distributions packagesummary.


Installation:
=============

The code run with no issues using Python versions 3.*.

Use the package manager pip to install Ola-Bino-Gaussian-Distributions

` pip install Ola-Bino-Gaussian-Distributions`


Contributors:
=============

Ajayi Olabode Olabode
