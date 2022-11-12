from flask import Flask, render_template, request, flash, redirect
import pickle
import numpy as np

app = Flask(__name__)

model = pickle.load(open("models/rf_model.pkl", "rb"))


def predict_default(features):
    features = np.array(features).astype(np.float64).reshape(1, -1)

    prediction = model.predict(features)
    probability = model.predict_proba(features)

    return prediction, probability


@app.route("/", methods=['GET', 'POST'])
def home():
    education_status = ["Graduate School", "University", "High School", "Others"]
    marital_status = ["Married", "Single", "Others"]

    payment_status = [
        "Account started that month with a zero balance, and never used any credit",
        "Account had a balance that was paid in full",
        "At least the minimum payment was made, but the entire balance wasn't paid",
        "Payment delay for 1 month",
        "Payment delay for 2 month",
        "Payment delay for 3 month",
        "Payment delay for 4 month",
        "Payment delay for 5 month",
        "Payment delay for 6 month",
        "Payment delay for 7 month",
        "Payment delay for 8 month",
    ]

    alert_message = False
    success_message = False

    try:
        if request.method == 'POST':

            features = request.form.to_dict()
            features['EDUCATION'] = education_status.index(features['EDUCATION']) + 1
            features['MARRIAGE'] = marital_status.index(features['MARRIAGE']) + 1
            features['PAY_1'] = payment_status.index(features['PAY_1']) - 2

            actual_feature_names = ['LIMIT_BAL', 'EDUCATION', 'MARRIAGE', 'AGE', 'PAY_1', 'BILL_AMT1', 'BILL_AMT2',
                                    'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6', 'PAY_AMT1', 'PAY_AMT2',
                                    'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6']
            feature_values = [features[i] for i in actual_feature_names]

            prediction, probability = predict_default(feature_values)
            if prediction[0] == 1:
                alert_message = "This account will be defaulted with a probability of {}%.".format(
                    round(np.max(probability) * 100, 2))
            else:
                success_message = "This account will not be defaulted with a probability of {}%.".format(
                    round(np.max(probability) * 100, 2))
    except:
        alert_message = "Please enter relevant information."

    return render_template("creditcard_default.html", education_status=education_status, marital_status=marital_status,
                           payment_status=payment_status, alert_message=alert_message, success_message=success_message)


if __name__ == '__main__':
    app.run(debug=True)





# import os
# import csv
# import shutil
# import pickle
# import numpy as np
# import pandas as pd
# from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file
# from flask_cors import CORS, cross_origin
#
# from prediction_validation_insertion import PredictionFilesValidation
# from predict_from_model import prediction
#
# app = Flask(__name__)
#
# app.config["csv_file"] = "Prediction_FinalResultFile/"
# app.config["sample_file"] = "Prediction_SampleFile/"
#
# model = None
# with open(str('models/random_forest.sav'), 'rb') as f:
#     model = pickle.load(f)
#
# @app.route('/')
# @cross_origin()
# def home():
#     return render_template('creditcard_default.html')
#
# @app.route('/return_sample_file/')
# @cross_origin()
# def return_sample_file():
#     sample_file = os.listdir("Prediction_SampleFile/")[0]
#     return send_from_directory(app.config["sample_file"], sample_file)
#
#
# @app.route('/return_file/')
# @cross_origin()
# def return_file():
#     final_file = os.listdir("Prediction_FinalResultFile/")[0]
#     return send_from_directory(app.config["csv_file"], final_file)
#
#
# @app.route('/result')
# @cross_origin()
# def result():
#     return render_template('result.html')
#
#
# @app.route('/predict_from_form', methods=['POST'])
# @cross_origin()
# def predict_from_form():
#     education_status = ["Graduate School", "University", "High School", "Others", "UnKnown"]
#     marital_status = ["Married", "Single", "Others"]
#
#     payment_status = [
#         "Account started that month with a zero balance, and never used any credit",
#         "Account had a balance that was paid in full",
#         "At least the minimum payment was made, but the entire balance wasn't paid",
#         "Payment delay for 1 month",
#         "Payment delay for 2 month",
#         "Payment delay for 3 month",
#         "Payment delay for 4 month",
#         "Payment delay for 5 month",
#         "Payment delay for 6 month",
#         "Payment delay for 7 month",
#         "Payment delay for 8 month",
#     ]
#
#     alert_message = False
#     success_message = False
#
#     try:
#         if request.method == 'POST':
#
#
#             features = request.form.to_dict()
#             print(features)
#             features['EDUCATION'] = education_status.index(features['EDUCATION']) + 1
#             features['MARRIAGE'] = marital_status.index(features['MARRIAGE']) + 1
#             features['PAY_1'] = payment_status.index(features['PAY_1']) - 2
#
#             actual_feature_names = ['LIMIT_BAL', 'EDUCATION', 'MARRIAGE', 'AGE', 'PAY_1', 'BILL_AMT1', 'BILL_AMT2',
#                                     'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6', 'PAY_AMT1', 'PAY_AMT2',
#                                     'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6']
#             feature_values = [features[i] for i in actual_feature_names]
#
#             prediction, probability = predict_default(feature_values)
#             if prediction[0] == 1:
#                 alert_message = "This account will be defaulted with a probability of {}%.".format(
#                     round(np.max(probability) * 100, 2))
#             else:
#                 success_message = "This account will not be defaulted with a probability of {}%.".format(
#                     round(np.max(probability) * 100, 2))
#     except:
#         alert_message = "Please enter relevant information."
#
#     return render_template("creaditcard_default.html", education_status=education_status, marital_status=marital_status,
#                            payment_status=payment_status, alert_message=alert_message, success_message=success_message)
#
#
# @app.route('/predict', methods=['POST'])
# @cross_origin()
# def predict():
#     if request.method == 'POST':
#         try:
#             if 'csvfile' not in request.files:
#                 return render_template("invalid.html")
#
#             file = request.files['csvfile']
#             df = pd.read_csv(file, index_col=[0])
#
#
#             path = 'Prediction_InputFileFromUser/'
#
#             if os.path.isfile('Prediction_InputFileFromUser/input_file.csv'):
#                 os.remove('Prediction_InputFileFromUser/input_file.csv')
#
#             df.to_csv('Prediction_InputFileFromUser/input_file.csv')
#
#             pred_obj = PredictionFilesValidation(path)  # object initialization
#             is_validated = pred_obj.prediction_validation()  # calling the training_validation function
#
#             if is_validated:
#                 pred = prediction(path)  # object initialization
#                 result = pred.predictionFromModel()
#                 result_df = pd.DataFrame(result, columns=["default_payment_next_month"])
#                 # print(result_df)
#
#                 final_df = pd.read_csv(path+"input_file.csv")
#                 final_df["default_payment_next_month"] = result_df
#
#                 if os.path.isfile('Prediction_FinalResultFile/Result.csv'):
#                     os.remove('Prediction_FinalResultFile/Result.csv')
#                 final_df.to_csv('Prediction_FinalResultFile/Result.csv', index=False)
#
#             else:
#                 return render_template('invalid.html')
#         except Exception as e:
#             raise e
#             # return render_template("invalid.html")
#
#
#
#     return redirect(url_for('result'))
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
#
#
#
