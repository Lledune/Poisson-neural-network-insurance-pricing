import tensorflow as tf
import keras 
import numpy as np 
import pandas as pd
from keras.layers import Dense
import keras.backend as KB
import math
from sklearn.metrics import mean_squared_error
from math import sqrt

data = pd.read_csv("c:/users/lucien/desktop/Poisson-neural-network-insurance-pricing/upsample.csv")

factors = data.drop('NumberClaims', axis = 1)
factors = factors.drop('ClaimFrequency', axis = 1)
nbClaims = data['NumberClaims']
nbClaims = nbClaims.to_frame()
y = data['ClaimFrequency']
d = data['Duration']
y = pd.DataFrame(y)
d = pd.DataFrame(d)
feed = np.append(y, d, axis = 1) #Used to pass d with y in loss function 
y = y.values
d = d.values

def rmse(yt, yp):
    rmse = sqrt(mean_squared_error(yt, yp))
    return rmse
    
def custom_loss(data, y_pred):

    y_true = data[:, 0]
    d = data[:, 1]
    # condition
    y_true = max(y_true, 0.00001)
    mask2 = keras.backend.greater(y_true, 0)
    mask2 = KB.cast(mask2, 'float32')

    # returns 0 when y_true =0, 1 otherwise
    #calculate loss using d...
    loss_value = (1-mask2) * 2 * d * y_pred + mask2 * (2 * d * (y_true * KB.log(y_true) - y_true * KB.log(y_pred + KB.epsilon()) - y_true + y_pred))
    return loss_value

    
def custom_loss2(data, y_pred):

    y_true = data[:, 0]
    d = data[:, 1]
    # condition
    def f1(d, y_pred): return 2 * d * y_pred
    def f2(d, y_true, y_pred): return 2 * d * (y_true * KB.log(y_true) - y_true * KB.log(y_pred) - y_true + y_pred)

    loss_value = tf.cond(KB.greater(y_true, 0), f1(d, y_pred), f2(d, y_true, y_pred))
    
    return loss_value

    def custom_loss3(data, y_pred):
        y_true = data[:, 0]
        d = data[:, 1]
        
        lnYTrue = KB.switch(KB.equal(y_true, 0), KB.zeros_like(y_true), KB.log(y_true))
        lnYPred = KB.switch(KB.equal(y_pred, 0), KB.zeros_like(y_pred), KB.log(y_pred))
        loss_value = 2 * d * (y_true * lnYTrue - y_true * lnYPred[:, 0] - y_true + y_pred[:, 0])
        return loss_value
    
    def deviance(data, y_pred):
        y_true = data[:, 0]
        d = data[:, 1]
        
        lnY = KB.log(y_true)
        bool1 = KB.equal(y_true, 0)
        zeros = KB.zeros_like(y_true)
        lnY = KB.switch(bool1, zeros, lnY)
        
        lnYp = KB.log(y_pred)
        bool2 = KB.equal(y_pred, 0)
        zeross = KB.zeros_like(y_pred)
        lnYp = KB.switch(bool2, zeross, lnYp)
        
        loss = 2 * d * (y_true * lnY - y_true * lnYp[:, 0] - y_true + y_pred[:, 0])
        return KB.sum(loss)


def baseline_model(loss):
    # create model
    #building model
    model = keras.Sequential()
    model.add(Dense(10, input_dim = 26, activation = "exponential"))
    model.add(Dense(5, input_dim = 26, activation = "exponential"))

    #model.add(Dense(10, activation = "relu"))
    model.add(Dense(1, activation = "exponential"))
    model.compile(loss=loss, optimizer='Adam')
    return model

model1 = baseline_model("mean_squared_error")
model2 = baseline_model(deviance)

model2.fit(factors, feed, epochs=4, shuffle=True, verbose=1)
model1.fit(factors, y, epochs=4, shuffle=True, verbose=1)

#model 1 = poisson, model 2 = custom
#In spyder IDE can check comp to see if two models are similar
import math 
preds1 = model1.predict(factors)
preds2 = model2.predict(factors)

compare1 = np.append(y, preds1, axis = 1)
compare1 = pd.DataFrame(compare1)

compare2 = np.append(y, preds2, axis = 1)
compare2 = pd.DataFrame(compare2)

comp = np.append(compare1, compare2, axis = 1)
comp = pd.DataFrame(comp)

compare3 = comp
#normalizing 0-1
from sklearn import preprocessing
x = compare3.values
MM = preprocessing.MinMaxScaler()
xScaled = MM.fit_transform(x)
compare3 = xScaled
compare3 = pd.DataFrame(compare3, columns=["a", "poisson", "c", "custom"])
compare3 = compare3.drop("c", axis = 1)





vect = np.vectorize(math.exp)
test = vect(preds)
test = pd.DataFrame(test)

rmse = rmse(y, preds)
test[127670:127680]
preds[127670:127680]
preds[3320:3330]
preds[69990:70000]
preds[100000:100020]
preds[0:20]


