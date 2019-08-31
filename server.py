import os
import pandas as pd
from sklearn.externals import joblib
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/predict', methods=['POST'])

def apicall():
    
    #pandas dataframe will be sent from this apicall
    
    try:
        testJson = request.get_json()
        test = pd.read_json(path_or_buf=testJson, orient= 'records')
        
        test['Dependents'] = [str(x) for x in list(test['Dependents'])]
        
        #Storing loan IDs seperately 
        
        loan_ids = test['Loan_ID']
        
    except Exception as e:
        raise e
        
    clf = 'loan_pred_prob_model_v1.pk'
    
    if test.empty:
        return(bad_request())
    else:
        print('Loading the model')
        with open('/Users/akash-mac/Desktop/My Docs/Self-Projects/Datasets/Loan Prediction Problem/'+clf, 'rb') as f:
        	loaded_model = pickle.load(f)
        
        print('The model has been loaded.......')
        print ('Doing predictions now.......')
        
        predictions = loaded_model.predict(test)
        
        prediction_series = list(pd.Series(predictions))
        final_predictions = pd.DataFrame(list(zip(loan_ids, prediction_series)))
        
        #sending response codes
        
        respones = jsonify(predictions = final_predictions.to_json(orient='records'))
        respones.status_code = 200
        
        return(respones)
