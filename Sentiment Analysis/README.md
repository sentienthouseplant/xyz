# About

Trained using Yelp Review dataset:
https://huggingface.co/datasets/fancyzhx/yelp_polarity

# Get started!

Make sure you have a csv of training data in the schema "positivity_class, text" where positivity_class is 1 for negative and 2 and for positive.

# Explanation of training.

The corpus of text is vectorised using the `TfidfVectorizer` included in the sklearn package - this roughly turns each text sample into a sparse vector which is the size of the signiciant vocabulary contained within the whole training data set. Occasionally, word which frequently appear together, like "absolutely amazing" or "really cool" will be turned into a single element of the vector.

A logistic linear regression model is fitted using the training sentiments and vectorised word samples. The predictions return a probability that the text is positive.

# API

The API allows you to ask for a prediction score given a piece of text. 