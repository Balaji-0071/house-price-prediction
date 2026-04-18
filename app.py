from flask import *
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import pickle

#load model
model = pickle.load(open('rf.pkl', 'rb'))

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/preview',methods=["POST"])
def preview():
    if request.method == 'POST':
        dataset = request.files['dataset']
        df = pd.read_csv(dataset,encoding = 'unicode_escape')
        df.set_index('Id', inplace=True)
        return render_template("preview.html",df_view = df)	

@app.route('/prediction',methods=['GET', 'POST'])
def prediction():
    return render_template('prediction.html')

@app.route('/predict',methods=['POST'])
def predict():
    feature = [x for x in request.form.values()]
    print("Input features:", feature)
    
    # Convert the input features to the correct format (pandas DataFrame)
    columns = ['location', 'bedroom', 'total_sqft', 'bath', 'balcony','price_per_sqft']  # Ensure these are in the correct order
    input_data = pd.DataFrame([feature], columns=columns)
    
    # Predict the result using the loaded model
    result = model.predict(input_data)
    return render_template('prediction.html', prediction_text= result)

@app.route('/performance')
def performance():
	return render_template('performance.html')  

@app.route('/chart')
def chart():
	return render_template('chart.html')  

if __name__ == "__main__":
    app.run(debug=True)