# Import necessary libraries
from openai import OpenAI  # For interacting with the OpenAI API
import json  # For JSON processing
from translate import Translator  # For translations
client = OpenAI()  # Initialize the OpenAI client

from flask import Flask, request, render_template  # Import Flask components for web app development
app = Flask(__name__)  # Initialize a Flask application

# Define a function to translate text to English using GPT-3.5
def translate_to_english(text):
    # Template prompt for language translation. The prompt outlines the task for GPT-3.5.
    template = """
         Identify the language of the input input_text: {}
        Output the language, code and english_translation in JSON format using the SCHEMA
        ...
    """
    prompt = template.format(text)  # Format the template with the input text

    # Call the OpenAI API with the formatted prompt
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful translator."},
            {"role": "user", "content": prompt}
        ]
      )
    
    print (template)  # Print the template (might not be necessary for production)
    print(response)  # Print the API response (might not be necessary for production)
    return response.choices[0].message.content  # Return the translation from the API response

# Function to get a generic response from GPT-3.5 based on the input text
def get_GPT_35_response(text):
    # Call the OpenAI API with the input text
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text}
        ]
      )
    return response.choices[0].message.content  # Return the response from the API

# Function to translate text from English to a specified language
def translate_from_english_to_input_language(text, code):
    translator = Translator(to_lang=code)  # Initialize the Translator with the target language code
    translation = translator.translate(text)  # Translate the text
    return translation  # Return the translated text

# Define a route for the root URL, displaying a form
@app.route('/')
def my_form():
    return render_template('my-form.html')  # Return the HTML form for user input

# Define a route for processing form submissions
@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']  # Extract the submitted text from the form

    # Get a raw response from GPT-3.5 for comparison
    raw_response = get_GPT_35_response(text)

    # Attempt to translate the submitted text to English
    try:
      translated_response = translate_to_english(text)
      # Clean up the translation output
      translated_response = translated_response.replace("```", "").replace("json", "").strip()

      json_dict = json.loads(translated_response)  # Parse the translation into a dictionary
      code = json_dict['code']  # Extract the language code
      english_translation = json_dict['english_translation']  # Extract the English translation
    except Exception as e:  # Handle errors during translation
      print(e)
      return "Error translating to English"

    # Get a GPT-3.5 response for the English translation
    gpt35_response_english_translation = get_GPT_35_response(english_translation)

    # Translate the GPT-3.5 response back to the original language
    translation_augmented_response = translate_from_english_to_input_language(gpt35_response_english_translation, code)
    
    # Build an HTML response to display the results
    HTMLRepsonse = "<html>" \
                   "<table border=5>" \
                   "<tr><td>Input</td><td>" + text + "</td></tr>" \
                   "<tr><td> raw response </td><td>" + raw_response + "</td></tr>" \
                   "<tr><td> translation augmented response  </td><td>" + translation_augmented_response + "</td></tr>" \
                   "</table>" \
                   "</html>"

    return HTMLRepsonse  # Return the HTML response