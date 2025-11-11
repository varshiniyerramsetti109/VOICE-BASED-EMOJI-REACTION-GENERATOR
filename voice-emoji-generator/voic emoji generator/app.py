from flask import Flask, render_template, request, jsonify
from textblob import TextBlob

# Initialize the Flask application
app = Flask(__name__)

@app.route('/')
def index():
    """Renders the main page."""
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_voice_command():
    """Processes the transcribed text to generate an emoji reaction."""
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({'emoji': '🤔', 'text': 'I did not hear anything.'})

    # Perform sentiment analysis using TextBlob
    blob = TextBlob(text)
    # Polarity is a float between -1.0 (very negative) and 1.0 (very positive)
    polarity = blob.sentiment.polarity

    # Determine the emoji based on the polarity score
    if polarity > 0.6:
        emoji = '😄'  # Very Positive
    elif polarity > 0.2:
        emoji = '😊'  # Positive
    elif polarity < -0.6:
        emoji = '😠'  # Very Negative
    elif polarity < -0.2:
        emoji = '🙁'  # Negative
    else:
        emoji = '😐'  # Neutral

    # Return the emoji and the original text as a JSON response
    return jsonify({'emoji': emoji, 'text': text})

if __name__ == '__main__':
    # Run the app in debug mode for development
    app.run(debug=True)