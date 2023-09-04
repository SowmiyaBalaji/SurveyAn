from flask import Flask, request, render_template
from pre_process import pre_process_file
import os
import joblib
from insights import generate_pdf
from send_mail import send_email
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    result = None
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files or 'email' not in request.form:
            return 'Invalid request'

        file = request.files['file']
        email = request.form['email']

        # If the user does not select a file, browser submits an empty part without filename
        if file.filename == '':
            return 'No selected file'

        # Save the file to a specific folder (e.g., 'uploads')
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        # Call the process_file function to get the processed data
        processed_data_0 = pre_process_file(file_path)

        processed_data = processed_data_0.drop(
            ['Emotion', 'Description'], axis=1)

        loaded_model = joblib.load(
            'C:\\Users\\admin\\OneDrive\\Desktop\\surveyan\\models\\random_forest_model.pkl')
        pred_val = []
        for index, row in processed_data.iterrows():
            # Assuming your processed_data DataFrame has a column named 'feature_column'
            feature = row['processed_text']
            # Convert the feature to a 1-dimensional input (e.g., a list or array)
            feature_input = [feature]
            # Make prediction using the loaded model
            prediction = loaded_model.predict(feature_input)
            type(prediction)
            pred_val.append(int(prediction))
            # Print the prediction for each row
        # Now you have the processed data, you can pass it to another function for prediction
        print(pred_val)
        generate_pdf(pred_val, processed_data_0)
        send_email(email, file_path)
        result = success()

        return render_template('result.html', prediction_result=result)

    return render_template('index.html')


def success():
    # Your prediction logic here
    # For example, you can use a trained model to make predictions based on the processed data

    prediction_result = "Survey Analysis sent to your mail"

    return prediction_result


if __name__ == '__main__':
    app.run(debug=True)
