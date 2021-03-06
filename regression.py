from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.cross_validation import KFold
import process_data as processed_data
# Sklearn also has a helper that makes it easy to do cross validation

# The columns we'll use to predict the target
predictors = ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"]

# Initialize our algorithm class
alg = LinearRegression()
# Generate cross validation folds for the titanic dataset.  It return the row indices corresponding to train and test.
# We set random_state to ensure we get the same splits every time we run this.
kf = KFold(processed_data.titanic.shape[0], n_folds=3, random_state=1)

predictions = []
for train, test in kf:
    # The predictors we're using the train the algorithm.  Note how we only take the rows in the train folds.
    train_predictors = (processed_data.titanic[predictors].iloc[train,:])
    # The target we're using to train the algorithm.
    train_target = processed_data.titanic["Survived"].iloc[train]
    # Training the algorithm using the predictors and target.
    alg.fit(train_predictors, train_target)
    # We can now make predictions on the test fold
    test_predictions = alg.predict(processed_data.titanic[predictors].iloc[test,:])
    predictions.append(test_predictions)

    # The predictions are in three separate numpy arrays.  Concatenate them into one.
# We concatenate them on axis 0, as they only have one axis.
predictions = np.concatenate(predictions, axis=0)

 # Map predictions to outcomes (only possible outcomes are 1 and 0)
predictions[predictions > .5] = 1
predictions[predictions <=.5] = 0
accuracy = sum(predictions[predictions == processed_data.titanic["Survived"]]) / len(predictions)
print(accuracy)