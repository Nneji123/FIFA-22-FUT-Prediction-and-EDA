# -*- coding: utf-8 -*-
"""FIFA 22 FUT Prediction and Exploratory Data Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13Q0byyPPZcmPpsJRSFysAvBR_PweavpY

# FIFA Ultimate Team Rating using Machine Learning

Import Required Libraries
"""

# Commented out IPython magic to ensure Python compatibility.
# Common imports
import numpy as np
import pandas as pd
import os
import seaborn as sns
from scipy import stats
import missingno as msno

# To plot pretty figures
# %matplotlib inline
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import style
sns.set(style='ticks', color_codes=True)
sns.set(style='darkgrid')
import plotly.express as px

# Ignore useless warnings (see SciPy issue #5998)
import warnings
warnings.filterwarnings(action="ignore", message="^internal gelsd")
warnings.filterwarnings('always')
warnings.filterwarnings('ignore')

"""Download the Dataset into our environment"""

! pip install -q kaggle
from google.colab import files

files.upload()

! mkdir ~/.kaggle

! cp kaggle.json ~/.kaggle/

! kaggle datasets download -d stefanoleone992/fifa-22-complete-player-dataset

! unzip fifa-22-complete-player-dataset.zip

fifa = pd.read_csv('players_22.csv')
fifa.head()

fifa.shape

fifa.columns

new_columns= ['overall','value_eur','attacking_crossing', 'attacking_finishing', 'attacking_heading_accuracy', 'attacking_short_passing', 'attacking_volleys', 'skill_dribbling', 'skill_curve', 'skill_fk_accuracy', 'skill_long_passing', 'skill_ball_control', 'movement_acceleration', 'movement_sprint_speed', 'movement_agility', 'movement_reactions', 'movement_balance', 'power_shot_power', 'power_jumping', 'power_stamina', 'power_strength', 'power_long_shots', 'mentality_aggression', 'mentality_interceptions', 'mentality_positioning', 'mentality_vision', 'mentality_penalties', 'mentality_composure', 'defending_standing_tackle', 'defending_sliding_tackle', 'goalkeeping_diving', 'goalkeeping_handling', 'goalkeeping_kicking', 'goalkeeping_positioning', 'goalkeeping_reflexes']
fifa_df=fifa[new_columns]
fifa_df.head()

fifa_df.describe()

fifa_df.shape

fifa_df.hist(bins=40, figsize=(27,17))
plt.show()

fifa_df.isna().any()

fifa_df.dropna(inplace=True)

fifa_df.head()

fifa_df.isna().any()

from sklearn.model_selection import train_test_split
train_set, test_set = train_test_split(fifa_df, test_size=0.2, random_state=42)
print("Length of training data:", len(train_set))
print("Length of testing data:", len(test_set))
print("Length of total data:", len(fifa_df))

fifa_df1 = train_set.copy()
corr_matrix = fifa_df.corr()
corr_matrix['overall'].sort_values(ascending=False)

from pandas.plotting import scatter_matrix
attributes = ['movement_reactions','mentality_composure','power_shot_power','value_eur','mentality_vision']
scatter_matrix(fifa_df[attributes], figsize=(15,12))
plt.show()

# Preparing the training and test set
y_train = train_set['overall']
X_train = train_set.drop('overall', axis=1)
y_test = test_set['overall']
X_test = test_set.drop('overall', axis=1)

from sklearn.linear_model import LinearRegression
lin_reg = LinearRegression()
lin_reg.fit(X_train, y_train)

predictions = lin_reg.predict(X_test)

print('Actual Overall:- ', y_test[0]) # Present Value of the House in dollars
print("Model Predicted Overall:-",predictions[0] )

from sklearn.metrics import mean_squared_error, r2_score

mse = mean_squared_error(y_test, predictions)
rmse=np.sqrt(mse)
print('Mean Squared Error= ', mse)
print('Root Mean Squared Error= ',rmse)

Rsquared=r2_score(y_test, predictions)
print('R^2 Value= ', Rsquared*100,'%')

from sklearn.tree import DecisionTreeRegressor
tree_reg = DecisionTreeRegressor()
tree_reg.fit(X_train, y_train)

y_predictions = tree_reg.predict(X_train)
tree_mse = mean_squared_error(y_train, y_predictions)
tree_rmse = np.sqrt(tree_mse)
tree_rmse

from sklearn.ensemble import RandomForestRegressor
forest_reg = RandomForestRegressor()
forest_reg.fit(X_train, y_train)

y_predictions = forest_reg.predict(X_train)
forest_mse = mean_squared_error(y_train, y_predictions)
forest_rmse = np.sqrt(forest_mse)
forest_rmse

from sklearn.model_selection import cross_val_score
scores = cross_val_score(lin_reg, X_train, y_train,scoring='neg_mean_squared_error', cv=10)
lin_reg_scores = np.sqrt(-scores)
def display_scores(scores):
  print("Scores:", scores)
  print("Mean:", scores.mean())
  print("Standard Deviation:", scores.std())
display_scores(lin_reg_scores)

scores = cross_val_score(tree_reg, X_train, y_train,
scoring='neg_mean_squared_error', cv=10)
tree_scores = np.sqrt(-scores)
display_scores(tree_scores)

scores = cross_val_score(forest_reg, X_train, y_train,
scoring='neg_mean_squared_error', cv=10)
forest_scores = np.sqrt(-scores)
display_scores(forest_scores)

from sklearn.model_selection import GridSearchCV
param_grid = [
{'n_estimators': [3, 10, 30], 'max_features': [2, 4, 6, 8]},
{'bootstrap': [False], 'n_estimators': [3,10], 'max_features': [2,3,4]},
]
forest_reg = RandomForestRegressor()
grid_search = GridSearchCV(forest_reg, param_grid, cv=5,
scoring='neg_mean_squared_error',
return_train_score=True)
grid_search.fit(X_train, y_train)

grid_search.best_params_

final_model = grid_search.best_estimator_
final_predictions = final_model.predict(X_test)
final_mse = mean_squared_error(y_test, final_predictions)
final_rmse = np.sqrt(final_mse)
final_rmse

confidence = 0.95
squared_errors = (final_predictions - y_test)**2
np.sqrt(stats.t.interval(confidence, len(squared_errors)-1,loc=squared_errors.mean(),
scale=stats.sem(squared_errors)))

some_data = X_test.iloc[:5]
some_label = y_test.iloc[:5]
print("Predictions:", final_model.predict(some_data))
print("Labels:", list(some_label))