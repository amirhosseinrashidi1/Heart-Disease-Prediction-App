Heart-Disease-Prediction-App:

This application uses a machine learning model to predict the likelihood of heart disease based on user input.
It is built with Python's Tkinter library for the
graphical user interface (GUI) and utilizes a pre-trained model and data stored in JSON and CSV files.




Features:
- Predict heart disease based on various health factors.
- Save user data and predictions to a CSV file.
- User-friendly GUI with placeholder text and tooltips.


Requirements:
  Python 3.x
  Tkinter
  NumPy
  scikit-learn
  pickle
  json
  csv



Usage:

**1.Run the application:**

**2.Input your details:**
   - Enter your name and age.
   - Fill in the other factors based on the form fields.

**3.Click "Predict" to see the result.**
  The prediction will be displayed in a message box. The result will also be saved in `people.csv`.

**4.Click "Clear" to reset the form.**


File Descriptions:

- `heart_disease_prediction.py`: The main script for running the application.
- `heart_disease_model.pkl`: The pre-trained machine learning model used for predictions.
- `factors.json`: JSON file containing the factors and their types used in the prediction form.
- `people.csv`: CSV file where user records and predictions are saved.
- `heart.png`: Logo image displayed in the application header.

License:
This project is licensed under the MIT License.

Acknowledgements:

- The machine learning model used in this project was trained with [scikit-learn](https://scikit-learn.org/).
- Special thanks to the contributors of the libraries and tools used in this project.
- with help : https://github.com/Mehdi1995m




