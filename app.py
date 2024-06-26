from flask import Flask, render_template, request
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

model_file_path = 'random_forest_regression_model.pkl'
model = None

try:
    with open(model_file_path, 'rb') as file:
        model = pickle.load(file)
except (EOFError, FileNotFoundError, pickle.UnpicklingError) as e:
    # Handle the error, print a message, or log it
    print(f"Error loading the model from {model_file_path}: {e}")

standard_to = StandardScaler()

@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    if model is None:
        return render_template('index.html', prediction_texts="Error: Model not loaded")

    try:
        Year = int(request.form['Year'])
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        Kms_Driven2 = np.log(Kms_Driven)
        Owner = int(request.form['Owner'])
        Fuel_Type_Petrol = request.form['Fuel_Type_Petrol']
        if Fuel_Type_Petrol == 'Petrol':
            Fuel_Type_Diesel = 0
        else:
            Fuel_Type_Diesel = 1

        Year = 2020 - Year
        Seller_Type_Individual = 1 if request.form['Seller_Type_Individual'] == 'Individual' else 0
        Transmission_Mannual = 1 if request.form['Transmission_Mannual'] == 'Mannual' else 0

        prediction = model.predict([[Present_Price, Kms_Driven2, Owner, Year, Fuel_Type_Diesel, 1 - Fuel_Type_Diesel,
                                     Seller_Type_Individual, Transmission_Mannual]])

        output = round(prediction[0], 2)

        if output < 0:
            return render_template('index.html', prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html', prediction_text=f"You Can Sell The Car at {output}")

    except Exception as e:
        # Print or log the exception for debugging
        print(f"Error in prediction: {e}")
        return render_template('index.html', prediction_texts="Error in prediction")

if __name__ == "__main__":
    app.run(debug=True)
