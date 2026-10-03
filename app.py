from pathlib import Path
import pickle

from flask import Flask, request, render_template
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent


def load_pickle(filename):
    with (BASE_DIR / filename).open("rb") as artifact:
        return pickle.load(artifact)


model = load_pickle("model.pkl")
scaler = load_pickle("standardscaler.pkl")
minmaxscaler = load_pickle("minmaxscaler.pkl")

# creating flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/predict",methods=['POST'])
def predict():
    field_names = (
        "Nitrogen",
        "Phosphorus",
        "Potassium",
        "Temperature",
        "Humidity",
        "Ph",
        "Rainfall",
    )
    try:
        feature_values = [float(request.form[name]) for name in field_names]
    except (KeyError, TypeError, ValueError):
        return render_template(
            "index.html",
            result="Sorry, enter a valid number for all seven soil and climate values.",
        ), 400

    feature_columns = ("N", "P", "K", "temperature", "humidity", "ph", "rainfall")
    single_pred = pd.DataFrame([feature_values], columns=feature_columns, dtype=float)
    scaled_features = minmaxscaler.transform(single_pred)
    final_features = scaler.transform(scaled_features)
    prediction = int(model.predict(final_features)[0])

    crop_dict = {1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
                 8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
                 14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
                 19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"}

    if prediction in crop_dict:
        crop = crop_dict[prediction]
        result = "{} is the best crop to be cultivated right there".format(crop)
    else:
        result = "Sorry, we could not determine the best crop to be cultivated with the provided data."
    return render_template("index.html", result=result)




# python main
if __name__ == "__main__":
    app.run(debug=True)