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
    # dump_this("StochasticGradientDescent", train_test, lambda i: SGDClassifier(i['loss'], i['penalty'], i['max_iter']
    # SGDClassifier(loss="hinge", penalty="l2", max_iter=5)
    # 'hinge', 'log', 'modified_huber',
    #         'squared_hinge', 'perceptron', or a regression loss: 'squared_loss',
    #         'huber', 'epsilon_insensitive', or 'squared_epsilon_insensitive'.

    for loss in ['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron', 'squared_loss', 'huber',
                 'epsilon_insensitive', 'squared_epsilon_insensitive']:
        for penalty in ['l2', 'l1', 'elasticnet']:
            for max_iter in range(1, 100):
                i = {'loss': loss, 'penalty': penalty, 'max_iter': max_iter}
                (acc, mae, prediction, model) = create_model(train_test, i, creator)
                if acc > max_acc:
                    result_model = model
                    result_mae = mae
                    max_acc = acc
                print("Acc = %f\t MAE = %f" % (acc, mae))
    print("Result Acc = %f\t MAE = %f" % (max_acc, result_mae))
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
    np.random.seed(0)
    print("\n\nDump " + name + " this ...")
    model = full_generation(name, train_test, creator)
    dump(model, 'trained/' + name + '.joblib')
    if hasattr(model, 'n_estimators'):
        print(name + " selected model with NEst = %d" % (model.n_estimators))
    else:
        print(name + " have no NEst")


np.random.seed(0)

training = pd.read_csv("full_set.csv")

# Create target and predictors variable
y = training.result
predictors = training.drop(['id', 'result'], axis=1)
print(predictors.columns)

## Split predictors and target variables into training and validation datasets

train_test = train_test_split(predictors, y, random_state=0)

dump_this("StochasticGradientDescent", train_test, lambda i: SGDClassifier(i['loss'], i['penalty'], i['max_iter']))