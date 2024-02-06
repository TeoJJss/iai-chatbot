import string, os, re, time
import spacy, asyncio
from autocorrect import Speller

nlp = spacy.load("en_core_web_md")
spell = Speller(lang='en')

async def reply(usr_inp):
    if os.path.isfile("config_sensitive.py"):
        from config_sensitive import get_qa
    else:
        from config import get_qa
    t=time.time()
    
    response = ""
    possible_answers = set()

    tmp_inp = str(usr_inp).lower().strip().translate(str.maketrans("", "", string.punctuation))
    inp = spell(tmp_inp)
    qa=await get_qa(inp, tmp_inp)
    print("input",inp, time.time()-t)
    if str(inp) in ["hi", "hello", "greetings", "hey"]:
        response = "Hi, I am APU Virtual Bot. You may ask me anything about the facilities and services in APU. "
    else:
        questions_inp_pairs = [(question, answer, inp) for answer, questions in qa.items() for question in questions]
        tasks = [similarity_worker(qip) for qip in questions_inp_pairs]
        results = await asyncio.gather(*tasks)
        possible_answers = {(q, a, s) for (q, a, s) in results if s > 0.8}

        print(time.time()-t)
        tmp_similarity = 0
        super_high = False
        if possible_answers:
            for ele in possible_answers:
                if not response.endswith("\n"):
                    response+="\n"

                if (int(ele[2]) >= 1):
                    if not super_high:
                        super_high=True
                        response = ""
                    tmp_similarity = ele[2]
                    if ele[1] not in response:
                        quest = ele[0]
                        response += ele[1] + "\n"
                elif abs(ele[2]-tmp_similarity) < 0.01:
                    tmp_similarity = ele[2]
                    if ele[1] not in response:
                        response += ele[1] + "\n\n"
                elif ele[2] > tmp_similarity:
                    quest, response, tmp_similarity = ele[0], ele[1], ele[2]
        else:
            response = "Sorry, I don't understand your question. I am still learning.\nPlease try another way to ask or refer to https://apiit.atlassian.net/wiki/spaces/KB/overview?mode=global."

        # Sort if many bus times
        if response.count("\n") > 2 and inp in ["bus schedule", "bus trip", "bus", "trip", "shuttle", "shuttle schedule"]:
            try:
                bus_list = [(line, line[-7:-2]) for line in response.strip().split('\n')]
                valid_times = [bus[1] for bus in bus_list if re.compile(r'\d{2}:\d{2}').match(bus[1])]
                if len(valid_times) == len(bus_list):
                    response = ""
                    sorted_bus_list = sorted(bus_list, key=lambda x: x[1])

                    for bus in sorted_bus_list:
                        response += bus[0] + "\n"
            except Exception as e:
                print("Error:", e)
        if not response.startswith("Sorry"):
            if quest != inp or inp != tmp_inp:
                response = f"> Guess you are asking: \"{quest}\"\n\n{response}" 
    print(f"bot: {response}", time.time()-t)
    return response

def calculate_similarity(query, response):
    query_doc = nlp(query)
    response_doc = nlp(response)
    similarity = query_doc.similarity(response_doc)
    if query.lower().strip() == response.lower().strip():
        print("exact match")
        similarity+=1
    return similarity

async def similarity_worker(args):
    question, ans, inp = args
    ques = spell(question.lower().strip())
    return question, ans, calculate_similarity(inp, ques)