# importing the library
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pickle

df=pd.read_parquet('test-sample.parquet')

# Removing the columns that are not necessary for the data modeling
# the columns that are not necessary are oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest (considering correlation result and multi-colinearity)
df.drop(['oldbalanceOrg','newbalanceOrig','oldbalanceDest','newbalanceDest'], axis = 1, inplace = True)

# nameDest and nameOrig can also be removed
df.drop(['nameOrig', 'nameDest'], axis = 1, inplace = True)

# encoding the categorical column into numerical data
le = LabelEncoder()
df['type'] = le.fit_transform(df['type'])

# assuming unknown fraud account, isFraud column  being dropped for testing purpose
X = df.drop('isFraud', axis = 1)
#y = df['isFraud']

# standardizing the data
sc = StandardScaler()
X = sc.fit_transform(X)

# Load the model
with open('decision_tree.pkl', 'rb') as file:
    sv = pickle.load(file)

# prediction using the load model
y_pred = sv.predict(X)

prediction=pd.merge(pd.DataFrame(y_pred,columns=['isFraud']),pd.read_parquet('test-sample.parquet').drop(columns=['isFraud']),how='left',left_index=True,right_index=True)
prediction=prediction[prediction['isFraud']==1]
prediction.to_csv('suspicious-cif.csv',index=False)