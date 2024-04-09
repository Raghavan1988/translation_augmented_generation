from openai import OpenAI
import json
from translate import Translator
client = OpenAI()

from flask import Flask, request, render_template
app = Flask(__name__)

"""
   Makes a GPT 3.5 call to translate the input text to English
"""
def translate_to_english(text):
    template = """
         Identify the language of the input input_text: {}
        Output the language, code and english_translation in JSON format using the SCHEMA
        SCHEMA:
            language: string,
            input_text: string,
            code: string,
            english_translation: string

        If the language matches one of the following in the list, use the code.
        Language - Code
    Afrikaans - af
    Albanian - sq
    Amharic - am
    Arabic - ar
    Armenian - hy
    Azerbaijani - az
    Basque - eu
    Belarusian - be
    Bengali - bn
    Bosnian - bs
    Bulgarian - bg
    Catalan - ca
    Cebuano - ceb
    Chichewa - ny
    Chinese (Simplified) - zh-cn
    Chinese (Traditional) - zh-tw
    Corsican - co
    Croatian - hr
    Czech - cs
    Danish - da
    Dutch - nl
    English - en
    Esperanto - eo
    Estonian - et
    Filipino - tl
    Finnish - fi
    French - fr
    Frisian - fy
    Galician - gl
    Georgian - ka
    German - de
    Greek - el
    Gujarati - gu
    Haitian Creole - ht
    Hausa - ha
    Hawaiian - haw
    Hebrew - he
    Hindi - hi
    Hmong - hmn
    Hungarian - hu
    Icelandic - is
    Igbo - ig
    Indonesian - id
    Irish - ga
    Italian - it
    Japanese - ja
    Javanese - jv
    Kannada - kn
    Kazakh - kk
    Khmer - km
    Kinyarwanda - rw
    Korean - ko
    Kurdish (Kurmanji) - ku
    Kyrgyz - ky
    Lao - lo
    Latin - la
    Latvian - lv
    Lithuanian - lt
    Luxembourgish - lb
    Macedonian - mk
    Malagasy - mg
    Malay - ms
    Malayalam - ml
    Maltese - mt
    Maori - mi
    Marathi - mr
    Mongolian - mn
    Myanmar (Burmese) - my
    Nepali - ne
    Norwegian - no
    Odia - or
    Pashto - ps
    Persian - fa
    Polish - pl
    Portuguese - pt
    Punjabi - pa
    Romanian - ro
    Russian - ru
    Samoan - sm
    Scots Gaelic - gd
    Serbian - sr
    Sesotho - st
    Shona - sn
    Sindhi - sd
    Sinhala - si
    Slovak - sk
    Slovenian - sl
    Somali - so
    Spanish - es
    Sundanese - su
    Swahili - sw
    Swedish - sv
    Tajik - tg
    Tamil - ta
    Tatar - tt
    Telugu - te
    Thai - th
    Turkish - tr
    Ukrainian - uk
    Urdu - ur
    Uyghur - ug
    Uzbek - uz
    Vietnamese - vi
    Welsh - cy
    Xhosa - xh
    Yiddish - yi
    Yoruba - yo
    Zulu - zu

    """

    prompt = template.format(text)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful translator."},
            {"role": "user", "content": prompt}
        ]
      )
    
    print (template)
    print(response)
    return response.choices[0].message.content

"""
   Makes a GPT 3.5 call to get a response
"""
def get_GPT_35_response(text):
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text}
        ]
      )
    return response.choices[0].message.content


def translate_from_english_to_input_language(text, code):
    translator = Translator(to_lang=code)
    translation = translator.translate(text)
    return translation

@app.route('/')
def my_form():
    return render_template('my-form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']

    ## Get Raw GPT 3.5 response for comparison
    raw_response = get_GPT_35_response(text)

    ## Translate to English
    try:
      translated_response = translate_to_english(text)
      translated_response = translated_response.replace("```", "")
      translated_response = translated_response.replace("json", "")
      translated_response = translated_response.strip()

      json_dict = json.loads(translated_response)
      code = json_dict['code']
      english_translation = json_dict['english_translation']
    except e as Exception:
      print(e)
      return "Error translating to English"    
    gpt35_response_english_translation = get_GPT_35_response(english_translation)
    ## Translate from English
    translation_augmented_response = translate_from_english_to_input_language(gpt35_response_english_translation, code)
    
   
    translated_response = translation_augmented_response

    HTMLRepsonse = "<html>"
    HTMLRepsonse += "<table border=5>"
    HTMLRepsonse += "<tr><td>Input</td><td>" + text + "</td></tr>"
    HTMLRepsonse += "<tr><td> raw response </td><td>" + raw_response + "</td></tr>"
    HTMLRepsonse += "<tr><td> translation augmented response  </td><td>" + translated_response + "</td></tr>"
    HTMLRepsonse += "</table>"
    HTMLRepsonse += "</html>"

    return HTMLRepsonse




