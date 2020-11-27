import numpy as np
import pandas as pd
from joblib import dump
from sklearn import svm
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier, ExtraTreesClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn import tree


# train_x, test_x, train_y, test_y = train_test_split(predictors, y, random_state=0)
def actualisation(train_test, start, end, creator):
    result_model = None  # Оверрайтнется энивей
    max_acc = 0
    for i in range(start, end, 20):
        (acc, mae, prediction, model) = create_model(train_test, i, creator)
        if acc > max_acc:
            result_model = model
            max_acc = acc
        print("Est =%d\t Acc = %f\t MAE = %f" % (i, acc, mae))
    return result_model

def full_generation(model_name, train_test, creator):
    print("\n\n" + model_name + " first build")
    model = actualisation(train_test, 300, 460, creator)

    if hasattr(model, 'n_estimators'):
        print(model_name + " with NEst = %d" % (model.n_estimators))
    else:
        print(model_name + " have no NEst")

    return model


# GradientBoostingClassifier(n_estimators=n_est, learning_rate=.05)
def create_model(train_test, i, creator):
    model = creator(i)
    model.fit(train_test[0], train_test[2])
    sc = model.score(train_test[1], train_test[3])
    prediction = model.predict(train_test[1])
    mae = mean_absolute_error(train_test[3], prediction)
    return (sc, mae, prediction, model)

def make_prediction(model, x, ids):
    return (model.predict(x))

def dump_this(name, train_test, creator):
    print("\n\nDump " + name + " this ...")
    model = full_generation(name, train_test, creator)
    dump(model, 'trained/'+name+'.joblib')
    if hasattr(model, 'n_estimators'):
        print(name + " selected model with NEst = %d" % (model.n_estimators))
    else:
        print(name + " have no NEst")


np.random.seed(0)

training = pd.read_csv("train.csv")

# Create target and predictors variable
y = training.result
predictors = training.drop(['id', 'result'], axis=1)
print(predictors.columns)

## Split predictors and target variables into training and validation datasets

train_test = train_test_split(predictors, y, random_state=0)

## MODELING
dump_this("GradientBoostingClassifier", train_test, lambda i: GradientBoostingClassifier(n_estimators=i, learning_rate=.05))

dump_this("RandomForest", train_test, lambda i: RandomForestClassifier(n_estimators=i))

dump_this("SupportVectorClassification", train_test, lambda i: svm.SVC())

dump_this("StochasticGradientDescent", train_test, lambda i: SGDClassifier())

#custom
dump_this("DecisionTreeClassifier", train_test, lambda i: tree.DecisionTreeClassifier())

dump_this("ExtraTreesClassifier", train_test, lambda i: ExtraTreesClassifier(n_estimators=i))