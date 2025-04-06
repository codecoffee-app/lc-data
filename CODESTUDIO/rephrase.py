from google import genai
import os
import json
import time

with open("../final-cs.json", 'r') as file:
    all = json.load(file)

i = 0
for item in all:
    i = i + 1
    if i <= 3039:
        continue
    if item["platform"] == "CODESTUDIO":
        try:    
            with open(f"./CODESTUDIO/{item['titleSlug']}.json", 'r') as file:
                data = json.load(file)

            if data['data']['question']["content"] == None:
                with open("contentNull.json",'r') as file:
                    k = json.load(file)
                    k.append({
                        "id" : i,
                        "slug": item["titleSlug"]
                    })
                    with open("contentNull.json",'w') as file:
                        json.dump(k, file, indent=4)
                continue

            client = genai.Client(api_key="AIzaSyAei3CvR9R4Qo1kWcMxbqvhJmG06f5kyHc")

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents="""
            This is the problem statement that i have in html form
            """ + data['data']['question']["content"] + """
            i want you to convert it into a json of below format and rephrase the body and explanation:
                    {
                        "body":"",
                        "constraints": [],
                        "testcases": [
                            {
                                "input":"",
                                "output":"",
                                "explanation": "if not present then null"
                            },
                            {
                                "input":"",
                                "output":"",
                                "explanation": "if not present then null"
                            }
                        ]
                    }
            if something is not available make it null. if there are images in the problem statement, then don't include them and any of its refrence
                    t""",
            )
            #print(response.text)
            response_text = response.text
            response_text = response_text.replace("```json","").replace("```","")
            try:
                response_json = json.loads(response_text) 
                rephrased = {
                    'body': response_json.get('body', None),
                    'constraints' : response_json.get('constraints', None),
                    'testcases' : response_json.get('testcases', None)
                }

                data['data']['question']['rephrased']=rephrased

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON response: {e}")
                break

            with open(f"{data['data']['question']['titleSlug']}.json", 'w') as file:
                    json.dump(data, file, indent=4)

        except Exception as e:
            print(e)
            print(f"Failed at {i}", item["titleSlug"])
            break
    print(i)
    time.sleep(2)