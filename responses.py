import string, os
import spacy
from autocorrect import Speller

nlp = spacy.load("en_core_web_md")

def reply(usr_inp):
    if os.path.isfile("config_sensitive.py"):
        from config_sensitive import get_qa
    else:
        from config import get_qa
    
    qa=get_qa()
    response = ""
    possible_answers = set()

    spell = Speller(lang='en')
    tmp_inp = str(usr_inp).lower().strip().translate(str.maketrans("", "", string.punctuation))
    inp = spell(tmp_inp)
    print("input",inp)
    if str(inp) in ["hi", "hello", "greetings", "hey"]:
        response = "Hi, I am APU Virtual Bot. You may ask me anything about the facilities in APU. -"
    else:        
        for answer, questions in qa.items():
            for question in questions:
                ques = question.lower().strip()
                # print(inp, ques)
                similarity = calculate_similarity(inp, spell(ques))

                if similarity > 0.6:
                    print(f"Debug - Question: {question}, Similarity: {similarity}")
                    possible_answers.add((question, answer, similarity))
        
        else:
            # Find the highest similarity ans among possible ans
            tmp_similarity = 0
            print(possible_answers)
            if possible_answers:
                for ele in possible_answers:
                    if ele[2] > tmp_similarity:
                        quest, response, tmp_similarity = ele[0], ele[1], ele[2]
                        print("question",quest)
                    elif round(ele[2], 4) == round(tmp_similarity, 4) or int(ele[2]) >= 1:
                        if ele[1] not in response:
                            response += "\n"+ele[1]
            else:
                response = "Sorry, I don't understand your question. I am still learning."

        if not response.startswith("Sorry"):
            if quest != inp or inp != tmp_inp:
                response = f"> Guess you are asking: \"{quest}\"\n\n{response}" 
    print(f"bot: {response}")
    return response

def calculate_similarity(query, response):
    query_doc = nlp(query)
    response_doc = nlp(response)
    similarity = query_doc.similarity(response_doc)
    return similarity