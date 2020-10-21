# Zillow Clustering Project

## Summary

**Goal**: What is driving the errors in the Zestimates?

For this project I will be working with the zillow dataset. Using the 2017 properties and predictions data for single unit / single family homes.

This project is meant to incorporate clustering methodologies.

My audience for this project is a data science team. The presentation will consist of a notebook demo of the discoveries I made and work I have done related to uncovering what the drivers of the error in the zestimate is.

Contents
- Report: Jupyter Notebook
- Python scripts to automate data acquisition and preparation process. Used in notebook

## Acquisition
`acquire.py`
Acquire data from the SQL data base. Credentials are stored in a personal env.py files
## Preparation
`prepare.py`
- acquire data from sql
- add county name
- filter for single unit properties
- drop description and other irrelevant columns
- drop columns/rows with over 60% missing values
- split the data into train, validate, test
- replaced nulls for categorical data with mode
- replaced nulls ofr continuous data with median
- renamed some columns for easier reading/writing
- separated continuous and cateorical features into two separate lists
## Exploration
`explore.py`
- visualized relationships with pairplot 
- run statistical test to see if the mean logerror significantly greater in Orange County vs all three counties
- run Kmeans clustering alorithms on 3 combinations of features to look for any patterns.
- Used elbow method and visualizations to determine k (clusters)
## Modeling
`model.py`
- split data to include variables that were relevant (continuous)
- scaled the data to use for modeling
- used a function to run RFE algorithm to select the top 5 features based on a linear regression model
- established a baseline mean for my target variable, logerror
- ran 4 different models: linear regression, lasso + lars, polynomial regression (squared), and polynomial regression (cubed)
- Evaluated the models and selected the top 3 to validate
- Tested my top model on unseen data
- Concluded with the linear regression model
## Conclusion
- I didn't find any useful clusters
    - more experience and is needed
    - incorporate encoding to be able to scale with other features
- log error doesn't have any obvious realtionship with my current features
    - It may have been helpful to explore more and create new features
- outliers should have been handled
    - they may have skewed the data enough to end up with bad models