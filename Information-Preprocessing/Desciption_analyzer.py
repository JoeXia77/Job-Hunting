import openai
import json
import os
import random

OPENAI_API_KEY = 'sk-12345'
openai.api_key = OPENAI_API_KEY

rule = """
You are an AI agent to extract useful information from the job description for job huntings. 
Generate a json file using the information you get from "job description". Here are the keys of the output json file, please try to complete the value of each key. Keys: 1. Job Title, 2. Level, 3. Qualified, 4. Skills, 5. Responsibilities, 6.years of experience required, 7.Company Name, 8. Company Goal}

Rules:
Describe the "Job Title" concisely and use alphabet only
Categorize the level of the job into: entry level, mid level, senior level.
Decide if I am not qualified for this job based on the following logic: "If this job for US citizen only, I am not qualified. If the job that do not require a computer science degree, I am not qualified. If the previous conditions are not mentioned, I am qualified. Answer in the json file Qualified part with yes or no. If answer No, give some concise clue within 20 words.
extract all the specific technical skills required in a format of keywords or tags and list them in json file Skill part. List programming languages used firstly in your output if exist, tools used second, and other techs used in the end of your output.
Answer the Company goal part in json file with some tags or key words, your result should try to explain the company type and its main product.
List all years of working experience required in a python list under as the content of "years of experience required" key in json file, make the result consice like ["x year -- field", ...]
Make the output in json format, reply only with the answer in json format, do not include any commentary. 

The following part is the "job description": 
"""


# ask for user input the job_description
job_description = """



About the job
Our Company

Changing the world through digital experiences is what Adobe’s all about. We give everyone—from emerging artists to global brands—everything they need to design and deliver exceptional digital experiences! We’re passionate about empowering people to create beautiful and powerful images, videos, and apps, and transform how companies interact with customers across every screen.

We’re on a mission to hire the very best and are committed to creating exceptional employee experiences where everyone is respected and has access to equal opportunity. We realize that new ideas can come from everywhere in the organization, and we know the next big idea could be yours!

Our Company

Changing the world through digital experiences is what Adobe’s all about. We give everyone—from emerging artists to global brands—everything they need to design and deliver exceptional digital experiences. We’re passionate about empowering people to craft beautiful and powerful images, videos, and apps, and transform how companies interact with customers across every screen.

We’re on a mission to hire the very best and are committed to building exceptional employee experiences where everyone is respected and has access to equal opportunity. We realize that new ideas can come from everywhere in the organization, and we know the next big idea could be yours!

The Opportunity

Adobe is looking for a Software Development Engineer to build a measurement system that openly collects user-experience interactions and provides metrics that drive concrete insights.

What you'll Do

Deliver best-in-class, responsive and scalable solutions ready for mass audiences.
Drive and implement a variety of innovative, critical initiatives using the latest tools and technologies.
Lead engineering initiatives across the stack while pairing with product and engineering partners throughout the company.
Design, develop, test, deploy and monitor features to enhance security, performance, cost-effectiveness, and User Experience.
Drive efforts to improve technical quality and solutions through code reviews, architecture reviews, and test suite strategy.
What you need to succeed

Passion for building: well thought through end-to-end solutions are second nature to you.
6+ years of professional experience building highly-performant and sophisticated web applications using modern web development technologies.
Professional experience with building for other developers: this can include APIs, SDKs, or libraries where technical users are the audience.
Experience working with large datasets, data pipelines, and a desire to work in these areas.
Ability to operate large scale data processing workflows.
Foundation in software engineering process & standard methodologies: testing, build automation, monitoring and observability technologies, CI/CD, etc.
Good written and verbal communication skills and English proficiency
Nice to have: cloud deployment strategies and knowledge of web performance optimizations.







"""


def preprocessing(content):
    ## delete special chars in Job Title 
    if 'Job Title' in content and content['Job Title']:
        content['Job Title'] = ''.join(ch for ch in content['Job Title'] if ch.isalpha() or ch.isspace())

    ## do the same thing for content['Company Name']
    if 'Company Name' in content and content['Company Name']:
        content['Company Name'] = ''.join(ch for ch in content['Company Name'] if ch.isalpha() or ch.isspace())
        

prompt = rule + job_description

messages=[{"role": "user", "content": prompt}]

response = openai.ChatCompletion.create(model="gpt-3.5-turbo",max_tokens=500,temperature=1.2,messages = messages)

response_content = response["choices"][0]["message"]["content"]

try:
    response_dict = json.loads(response_content)
except json.JSONDecodeError:
    print("The response content is not in valid JSON format.")
    response_dict = {}

preprocessing(response_dict)

print(response_content)

# let user input 'n' or 'y' about whether the user will consider this job
user_input = input("Would you consider this job? (y/n): ")

# Ensure 'Consider' and 'Other' directories exist
os.makedirs('Consider', exist_ok=True)
os.makedirs('Other', exist_ok=True)

company = response_dict.get('Company Name', 'unknown')
job_title = response_dict.get('Job Title', 'unknown')

# If company or job_title is unknown, add a random number for uniqueness
if company == 'unknown' or job_title == 'unknown':
    rand_num = random.randint(1000,9999)  # generate a random number between 1000 and 9999
    json_file_name = f"{company} - {job_title} - {rand_num}.json"
else:
    json_file_name = f"{company} - {job_title}.json"
    

if user_input.lower() == 'y':
    address = input("Enter an url for future reference")
    response_dict['address'] = address
    # if input y, save it as a json file in a folder called "Consider"
    with open(os.path.join('Consider', json_file_name), 'w') as json_file:
        json.dump(response_dict, json_file)
else:
    # if input is n, save it to a folder called "Other"
    with open(os.path.join('Other', json_file_name), 'w') as json_file:
        json.dump(response_dict, json_file)
