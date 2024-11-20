from flask import Flask, render_template, request, jsonify
import pickle
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Initialize PorterStemmer
ps = PorterStemmer()

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Text preprocessing function
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
    
    text = y[:]
    y.clear()
    
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
            
    text = y[:]
    y.clear()
    
    for i in text:
        y.append(ps.stem(i))
    
    return " ".join(y)

# Load vectorizer and model
tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    message = request.json.get('message')  # Get JSON data from the request
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Preprocess the input message
    transformed_message = transform_text(message)
    
    # Vectorize the message
    vector_input = tfidf.transform([transformed_message])
    
    # Predict using the loaded model
    prediction = model.predict(vector_input)[0]
    
    # Determine if spam or not
    result = "Spam" if prediction == 1 else "Not Spam"
    
    return jsonify({'prediction': result})  # Send result as JSON response

if __name__ == '__main__':
    app.run(debug=True)
