import openai
import requests


## Papago translator Area
papago_cliend_id = "[YOUR PAPAGO CLIENT ID]"
papago_cliend_secret = "[YOUR PAPAGO CLIENT SECRET ID]"

def get_translate(text, source_lang, target_lang):
    client_id = papago_cliend_id
    client_secret = papago_cliend_secret

    data = {'text' : text,
            'source' : source_lang,
            'target': target_lang}

    url = "https://openapi.naver.com/v1/papago/n2mt"

    header = {"X-Naver-Client-Id":client_id,
              "X-Naver-Client-Secret":client_secret}

    response = requests.post(url, headers=header, data=data)
    rescode = response.status_code

    if(rescode==200):
        send_data = response.json()
        trans_data = (send_data['message']['result']['translatedText'])
        return trans_data
    else:
        print("Error Code:" , rescode)



##Tarot reading AI Area

openai.api_key = "[YOUR OPENAI API KEY]"



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
    topic = get_translate(ask_topic, "ko", "en")
    question = get_translate(ask, "ko", "en")
    card = sel_card

    print(topic)
    print(question)
    print(card)

    prompt = f'''You are a tarot card reader.
            Please answer {question} within the scope of {topic} using the interpretation of the selected card.
            The selected card is the {card}.
            Your answer should include explanation of the imagess in the selected card'''
    
    answer = tarot_answer(prompt).choices[0].text.strip('.\n\n')
    print(answer)


    return get_translate(answer, "en", "ko")
