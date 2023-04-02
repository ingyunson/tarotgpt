import openai
import os
from google.cloud import translate_v2 as translate

## Google translator area

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '[YOUR KEY.json]'
client = translate.Client()

def get_translate(text, target_lang):
    client = translate.Client()
    result = client.translate(text, target_language=target_lang)
    
    return result



##Tarot reading open AI Area

openai.api_key = "[YOUR OPEN AI API KEY]"



def tarot_answer(prompt):        
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=4000,
        top_p=0.3,
        frequency_penalty=0.5,
        presence_penalty=0
    )

    return response

def tarot_ask(ask, ask_topic, sel_card):
    topic = get_translate(ask_topic, "en")['translatedText']
    question = get_translate(ask, "en")['translatedText']
    card = sel_card

    print(topic)
    print(question)
    print(card)

    prompt = f'''You are a tarot card reader.
            Please answer {question} within the scope of {topic} using the interpretation of the selected card.
            The selected card is the {card}.
            Your answer should include explanation of the imagess in the selected card'''
    
    answer = tarot_answer(prompt).choices[0].text.strip('.\n\n')

    
    return get_translate(answer, "ko")['translatedText']

