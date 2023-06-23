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
Decide if I am not qualified for this job based on the following logic: "If this job for US citizen only, I am not qualified. If the job that do not require a computer science degree, I am not qualified. If job description mentioned sponsorship is not provided, I am not qualified. If the previous conditions are not mentioned, I am qualified. Answer in the json file Qualified part with yes or no. If answer No, give some concise clue within 20 words.
extract all the specific technical skills required in a format of keywords or tags and list them in json file Skill part. List programming languages used firstly in your output if exist, tools used second, and other techs used in the end of your output.
Answer the Company goal part in json file with some tags or key words, your result should try to explain the company type and its main product.
List all years of working experience required in a python list under as the content of "years of experience required" key in json file, make the result consice like ["x year -- field", ...]
Make the output in json format, reply only with the answer in json format, do not include any commentary. 

The following part is the "job description": 
"""


# ask for user input the job_description
job_description = """








About the job
Why will you enjoy this new opportunity?

Work on bleeding edge Kubernetes deployments and solutions.
Opportunity to work on telco scale problems.
Distributed and cloud-native product architecture.
Freedom to innovate and explore efficient solutions.

Success in the Role: What are the performance outcomes over the first 6-12 months you will work toward completing?

Demonstrate eagerness to learn and master Kubernetes and Cloud-native deployment and infrastructure.
Innovate continuously and help the product continue to lead in the telco automation and orchestration space.
Design and develop high-quality software.

The Work: What type of work will you be doing? What assignments, requirements, or skills will you be performing on a regular basis?

Hands-on development, and design of critical modules for the Telco Cloud Automation Product.
Work closely with architects, different teams, and QEE to develop innovative and efficient infrastructure automation solutions
Work across multiple VMware product teams and develop inclusive solutions.

What is the leadership like for this role? What is the structure and culture of the team like?

Work as an individual contributor and work in a small team of 4-5 engineers.
You will work under a tech lead or an architect and work on a module.
Customer-focused and detail-oriented team culture.

Where is this role located?

Flexible/Remote: The role is considered flexible and will be a mix of working from a local VMware office and/or remote depending on your preferences and the arrangements determined with your future manager.

What are the benefits and perks of working at VMware?

You and your loved ones will be supported with a competitive and comprehensive benefits package. Below are some highlights, or you can view the complete benefits package by visiting www.benefits.vmware.com.

Medical Coverage, Retirement, and Parental Leave Plans for All Family Types
Generous Time Off Programs
40 hours of paid time to volunteer in your community
Rethink's Neurodiversity program to support parents raising children with learning or behavior challenges, or developmental disabilities
Financial contributions to your ongoing development (conference participation, trainings, course work, etc.)
Wellness reimbursement and online fitness and wellbeing classes

For US based candidates, the annual pay range (OTE for commissioned roles; Salary for other roles) for this position is: $84,000 - $190,000. The actual offer will be based on the role, location, and individual candidate experience. Bonus, commission, and/or equity may be eligible for this position. VMware offers comprehensive benefits including, but not limited to: medical, dental, and vision plans, company paid holidays, paid sick leave, and vacation time. Additional benefits for this position can be found at https://benefits.vmware.com/. Your talent advisor can share more about the specific salary range for your preferred location during the hiring process.

This job may require the candidate to travel and/or work from a facility that requires full vaccination prior to entry.

Category : Engineering and Technology

Subcategory: Software Engineering

Experience: Manager and Professional











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
