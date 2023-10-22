@randomForest_Route.route("/programOneRow", methods=["GET", "POST"])
def programOneRow():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))

    if request.method == "POST":
        # Get user inputs from the form
        Kasarian = request.form['Kasarian']
        Edad = request.form['Edad']
        Antas_na_tinapos = request.form['Antas na tinapos']
        Uri_ng_trabaho = request.form['Uri ng trabaho']
        Pangedukasyon = request.form.get('Pangedukasyon', '0')
        Pangkultura = request.form.get('Pangkultura', '0')
        Pangkabuhayan = request.form.get('Pangkabuhayan', '0')
        Values_at_Moral = request.form.get('ValuesMoral', '0')
        Pagtatanim = request.form.get('Pagtatanim', '0')
        Ayudang_Pagkain = request.form.get('Pagkain', '0')
        Pangkalusugan = request.form.get('Pangkalusugan', '0')
        Pagrerecycle = request.form.get('Pagrerecycle', '0')
        Dental = request.form.get('Dental', '0')
        Teknolohiya = request.form.get('Teknolohiya', '0')

        # Create a list of user inputs
        user_inputs = [Kasarian, Edad, Antas_na_tinapos, Uri_ng_trabaho, Pangedukasyon, Pangkultura,
                       Pangkabuhayan, Values_at_Moral, Pagtatanim, Ayudang_Pagkain, Pangkalusugan,
                       Pagrerecycle, Dental, Teknolohiya]

        # Create a DataFrame from user inputs
        user_df = pd.DataFrame([user_inputs], columns=feature_columns)

        # Create an imputer with the 'mean' strategy
        imputer = SimpleImputer(strategy='mean')

        # Fit the imputer on your user input data and transform it
        user_df_imputed = pd.DataFrame(imputer.fit_transform(user_df), columns=feature_columns)

        # Use the trained model to make predictions on the imputed data
       
        predictions = model1.predict(user_df_imputed)

        # Render the result page with predictions
        return render_template("result.html", predictions=predictions)
    return render_template("program.html")

    

    #Machine learning
# Define the column names for the features
feature_columns = ['Kasarian', 'Edad', 'Antas na tinapos', 'Uri ng trabaho', 
                   'Pangedukasyon', 'Pangkultura', 'Pangkabuhayan', 'Values at Moral', 
                   'Pagtatanim', 'Ayudang Pagkain', 'Pangkalusugan', 'Pagrerecycle', 'Dental', 'Teknolohiya']


@randomForest_Route.route("/programWithCSV", methods=["GET", "POST"])
def programWithCSV():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))

    if request.method == "POST":
        csv_file = request.files["csv_file"]

        if csv_file:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(csv_file)

            # Check if any columns have data type 'object' (strings)
            columns_with_strings = df.select_dtypes(include=['object']).columns

             # Create a dictionary to store sub-programs for each program
             # Create a dictionary to store sub-programs for each program
            sub_programs_dict = {
                "Literacy": ["Sub-Program A", "Sub-Program B"],
                "Socio-economic": ["Sub-Program C", "Sub-Program D"],
                "Environmental Stewardship": ["Sub-Program E", "Sub-Program F"],
                "Health and Wellness": ["Sub-Program G", "Sub-Program H"],
                "Cultural Enhancement": ["Sub-Program I", "Sub-Program J"],
                "Values Formation": ["Sub-Program K", "Sub-Program L"],
                "Disaster Management": ["Sub-Program M", "Sub-Program N"],
                "Gender Development": ["Sub-Program O", "Sub-Program P"]
                # You can add more sub-programs for each program as needed
            }

            if not columns_with_strings.empty:
                # Define encoding dictionaries
                encoding_dict_kasarian = {'Male': 0, 'Female': 1}
                encoding_dict_edad = {'17-below': 0, '18-24': 1, '25-34': 2, '35-44': 3, '45-54': 4, '55-64': 5, '65-Above': 6}
                encoding_dict_antas = {'Elementary': 0, 'Not Elementary': 1, 'Secondary': 2, 'Not Secondary': 3, 'College': 4,
                                       'Not College': 5, 'Masters Degree': 6, 'Doctorate Degree': 7, 'Uneducated': 8}
                encoding_dict_uri = {'Employed': 0, 'Unemployed': 1}

                # Map string values to numerical values in columns with 'object' data type
                df['Kasarian'] = df['Kasarian'].map(encoding_dict_kasarian)
                df['Edad'] = df['Edad'].map(encoding_dict_edad)
                df['Antas na tinapos'] = df['Antas na tinapos'].map(encoding_dict_antas)
                df['Uri ng trabaho'] = df['Uri ng trabaho'].map(encoding_dict_uri)

                # Assuming other columns (Pangedukasyon, Pangkultura, etc.) also need encoding,
                # add similar mapping code here

            # Now, you can use the DataFrame for predictions
            if "Program" in df.columns:
                target_variable = "Program"
                X = df.drop(target_variable, axis=1)  # Features
                y = df[target_variable]  # Target

                # Use your trained model to make predictions on the features
                predictions = model1.predict(X)

                # Add the predictions to the DataFrame
                df["Predictions"] = predictions

            else:
                # If the "Program" column is not present, assume all columns are features
                # Use your trained model to make predictions on the entire DataFrame
                predictions = model1.predict(df)

                # Create a new column for predictions in the DataFrame
                df["Predictions"] = predictions

            # Count the frequency of each prediction
            prediction_counts = Counter(predictions)

            # Find the top 3 most frequent predictions
            top_3_predictions = prediction_counts.most_common(3)

             # Pass the top programs and their sub-programs to the template
            top_programs_with_subprograms = []
            for prediction, count in top_3_predictions:
                top_programs_with_subprograms.append({
                    "program": prediction,
                    "quantity": count,
                    "sub_programs": sub_programs_dict.get(prediction, [])
                })

            # ...
            return render_template("resultCSV.html",
                       top1=top_programs_with_subprograms[0] if len(top_programs_with_subprograms) >= 1 else {},
                       top2=top_programs_with_subprograms[1] if len(top_programs_with_subprograms) >= 2 else {},
                       top3=top_programs_with_subprograms[2] if len(top_programs_with_subprograms) >= 3 else {})
    return render_template("program.html")


Literacy_subprogram = session.query(Subprogram).filter(Subprogram.subprogram == "Literacy").all()
            Socio_subprogram = session.query(Subprogram).filter(Subprogram.subprogram == "Socio-economic").all()
            Environmental_subprogram = session.query(Subprogram).filter(Subprogram.subprogram == "Environmental Stewardship").all()
            Health_subprogram = session.query(Subprogram).filter(Subprogram.subprogram == "Health and Wellness").all()
            Cultural_subprogram = session.query(Subprogram).filter(Subprogram.subprogram == "Cultural Enhancement").all()
            Values_subprogram = session.query(Subprogram).filter(Subprogram.subprogram == "Values Formation").all()
            Disaster_subprogram = session.query(Subprogram).filter(Subprogram.subprogram == "Disaster Management").all()
            Gender_subprogram = session.query(Subprogram).filter(Subprogram.subprogram == "Gender and Development").all()



            sub_programs_dict = {
                "Literacy": [Literacy_subprogram],
                "Socio-economic": [Socio_subprogram],
                "Environmental Stewardship": [Environmental_subprogram],
                "Health and Wellness": [Health_subprogram],
                "Cultural Enhancement": [Cultural_subprogram],
                "Values Formation": [Values_subprogram],
                "Disaster Management": [Disaster_subprogram],
                "Gender and Development": [Gender_subprogram]
                # You can add more sub-programs for each program as needed
            }