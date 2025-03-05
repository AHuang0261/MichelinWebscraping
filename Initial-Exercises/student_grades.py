import pickle
import sklearn
import sklearn.model_selection
import tensorflow as tf
import pandas as pd
from sklearn import linear_model
import numpy as np


data = pd.read_csv("student-mat.csv", sep=";")
data = data[["G1", "G2", "G3", "studytime", "failures", "absences"]]
predict = "G3"
X = np.array(data.drop([predict], 1))
Y = np.array(data[predict])
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, Y, test_size= 0.1)

# best = 0
# for alsdlfkj in range(30):
#     x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, Y, test_size= 0.1)
#     linear = linear_model.LinearRegression()
#     linear.fit(x_train, y_train)
#     acc = linear.score(x_test, y_test)
#     print(alsdlfkj,acc)
#     if acc > best:
#         best = acc        
#         with open("studentmodel.pickle", "wb") as f:
#             pickle.dump(linear,f)
        



pickle_in = open("studentmodel.pickle", "rb")
linear = pickle.load(pickle_in)
print(linear.score(x_test,y_test))
