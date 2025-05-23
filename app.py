from flask import Flask, request, render_template, redirect, url_for, session
import pickle
from deep_translator import GoogleTranslator  # for translation

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Load model, vectorizer, and disease info
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("disease_info.pkl", "rb") as f:
    disease_info = pickle.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['symptoms'].strip()
        language = request.form.get('language', 'en')

        if user_input:
            try:
                # Translate user input to English if not English
                if language != 'en':
                    translated_input = GoogleTranslator(source=language, target='en').translate(user_input)
                else:
                    translated_input = user_input

                symptoms = [translated_input]
                vectorized_input = vectorizer.transform(symptoms)
                predicted_disease = model.predict(vectorized_input)[0]

                info = disease_info.get(predicted_disease, {})
                medicine = info.get('medicine', 'Not available')
                diet = info.get('diet', 'Not available')

                # Translate results back to user's language if needed
                if language != 'en':
                    predicted_disease = GoogleTranslator(source='en', target=language).translate(predicted_disease)
                    medicine = GoogleTranslator(source='en', target=language).translate(medicine)
                    diet = GoogleTranslator(source='en', target=language).translate(diet)

                # Save result in session temporarily
                session['result'] = {
                    'disease': predicted_disease,
                    'medicine': medicine,
                    'diet': diet,
                    'symptoms': user_input  # keep original user input
                }

                return redirect(url_for('index'))

            except Exception as e:
                session['result'] = {'error': f"Error: {str(e)}"}
                return redirect(url_for('index'))

        else:
            session['result'] = {'error': 'Please enter symptoms to get diagnosis.'}
            return redirect(url_for('index'))

    result = session.pop('result', None)  # Clear result after displaying once
    symptoms = result.get('symptoms') if result else ''
    return render_template('index.html', result=result, symptoms=symptoms)


if __name__ == '__main__':
    app.run(debug=True)
