# translation_augmented_generation
Simple Technique that improves GPT 3.5's resposne quality in non english languages with simple translation


# Unlock LLMs for a Billion more Prompt Engineers

##update 11/2023
I presented the findings of this hackathon at DSS Salon SF conference


https://docs.google.com/presentation/d/1i1MM0KVZUJ6bruba_MxREEA8suwCOvAD/edit#slide=id.p24

Link : https://www.datascience.salon/san-francisco/schedule/

GPT performs much better following instructions when translated in English
1. pip install -r requirements.txt
2. export FLASK_APP= <file_name.py>
3. flask run

## Example in Tamil
Prompt: சூரியனில் இருந்து பூமிக்கு ஒளி பயணிக்க எவ்வளவு நேரம் ஆகும்
(english): How long does it take for light to travel from the sun to the earth?
You can see without translation, the GPT 3.5 response is not accurate. It did not get the answer of 8 min 20 seconds
with translation layer, GPT 3.5 response is accurate. It got the answer of 8 minutes 20 seconds
![Screenshot from 2024-04-08 23-06-37](https://github.com/Raghavan1988/translation_augmented_generation/assets/493090/c58a1d7f-0ac8-4287-bb6f-812260ad69f6)
