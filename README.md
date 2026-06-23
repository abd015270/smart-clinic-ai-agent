\# Smart Clinic AI Agent



Smart Clinic AI Agent is an AI-powered clinic assistant that helps patients find suitable clinics, check doctor availability, book appointments, ask clinic-related questions, and send emergency alerts.



This project was built as an AI startup final project. It includes a real AI Agent with tools, RAG, Skills, Evals, Streamlit demo, and a business plan.



\---



\## Project Idea



Small and medium medical clinics waste many hours every week answering repeated questions, checking appointments manually, and handling booking requests.



Smart Clinic AI Agent solves this problem by acting as a digital clinic assistant that can:



\* Search for clinics by city and specialty

\* Check doctor availability

\* Book appointments

\* Generate booking codes

\* Answer clinic FAQ and booking policy questions

\* Register emergency alerts

\* Display appointments and emergency alerts in a dashboard



\---



\## Main Features



\* Real AI Agent using CrewAI

\* Agent role, goal, and backstory

\* Multiple custom tools

\* RAG knowledge base

\* Skills file using SKILL.md

\* SQLite database

\* Streamlit live demo

\* Evaluation tests with 5 test cases

\* Business cost estimator

\* Business plan

\* Pitch script

\* Presentation content



\---



\## Technologies Used



\* Python 3.11

\* CrewAI

\* Streamlit

\* OpenAI API

\* SQLite

\* Pandas

\* Python Dotenv

\* JSON

\* Markdown



\---



\## Project Structure



```text

smart-clinic-ai-agent/

│

├── app.py

├── main.py

├── requirements.txt

├── README.md

├── .env.example

│

├── data/

│   ├── clinics.json

│   ├── doctors.json

│   └── appointments.db

│

├── knowledge\_base/

│   ├── clinic\_faq.md

│   ├── booking\_policy.md

│   └── emergency\_guidelines.md

│

├── skills/

│   └── clinic\_agent\_skill/

│       └── SKILL.md

│

├── src/

│   ├── agent.py

│   ├── tools.py

│   ├── rag.py

│   ├── database.py

│   ├── config.py

│   └── utils.py

│

├── evals/

│   ├── eval\_cases.json

│   └── run\_evals.py

│

├── business/

│   ├── business\_plan.md

│   └── pitch\_script.md

│

└── presentation/

&#x20;   └── slides\_content.md

```



\---



\## Setup Instructions



\### 1. Create virtual environment



```powershell

py -3.11 -m venv venv

```



\### 2. Activate virtual environment



```powershell

.\\venv\\Scripts\\activate

```



\### 3. Install dependencies



```powershell

pip install -r requirements.txt

```



\### 4. Configure environment variables



Create a `.env` file based on `.env.example`.



```env

OPENAI\_API\_KEY=your\_openai\_api\_key\_here

OPENAI\_MODEL=gpt-4o-mini

```



Important: do not upload the `.env` file to GitHub.



\---



\## Run the Project



\### Initialize the database



```powershell

python main.py

```



Expected output:



```text

Smart Clinic AI Agent project initialized successfully.

Database is ready.

```



\### Run the AI Agent test



```powershell

python -m src.agent

```



This runs a test request:



```text

I am Ahmad, my phone is 0599999999. I need a dentist in Nablus and I prefer Saturday 10:30. Please book an appointment.

```



Expected result:



\* Clinic found

\* Doctor found

\* Appointment booked

\* Booking code generated



\### Run the Streamlit demo



```powershell

streamlit run app.py

```



Then open:



```text

http://localhost:8501

```



\---



\## Streamlit Demo Pages



The demo includes:



1\. AI Agent Chat

&#x20;  Runs the real CrewAI Agent.



2\. Find Clinic

&#x20;  Searches clinics by city and specialty.



3\. Book Appointment

&#x20;  Books appointments and generates booking codes.



4\. Emergency Alert

&#x20;  Sends emergency alerts to clinics that support emergency cases.



5\. Knowledge Base RAG

&#x20;  Retrieves information from local knowledge files.



6\. Business Cost

&#x20;  Estimates monthly operating cost.



7\. Dashboard

&#x20;  Displays appointments and emergency alerts.



\---



\## Agent Details



The project includes a real AI Agent.



\### Role



Smart Clinic Patient Assistant



\### Goal



Help patients find the right clinic, understand clinic policies, book appointments, and send emergency alerts when needed.



\### Backstory



The agent acts as an experienced digital clinic assistant that supports small and medium medical clinics.



\### Tools



The agent uses the following tools:



\* Clinic Search Tool

\* Doctor Availability Tool

\* Appointment Booking Tool

\* Clinic Knowledge Tool

\* Emergency Alert Tool

\* Cost Estimator Tool



\---



\## RAG Knowledge Base



The RAG system searches local Markdown files:



\* `clinic\_faq.md`

\* `booking\_policy.md`

\* `emergency\_guidelines.md`



It is used when the patient asks about:



\* Booking rules

\* Cancellation policy

\* Clinic FAQ

\* Emergency guidelines

\* Safety rules



\---



\## Skills



The project includes:



```text

skills/clinic\_agent\_skill/SKILL.md

```



This file teaches the agent how to behave as a professional clinic assistant.



The skill includes:



\* Booking behavior

\* Emergency behavior

\* Safety rules

\* Response style

\* Medical diagnosis restrictions



\---



\## Evals



The project includes 5 evaluation cases:



1\. Book dentist appointment in Nablus

2\. Ask about cancellation policy

3\. Emergency alert in Nablus

4\. Find pediatric clinic in Ramallah

5\. Ask if AI replaces doctor



Run evals:



```powershell

python -m evals.run\_evals

```



Current result:



```text

Passed: 5/5

Success Rate: 100.0%

```



\---



\## Business Model



The project uses a monthly subscription model for small and medium clinics.



Suggested pricing:



\* Basic Plan: $29 per clinic per month

\* Pro Plan: $59 per clinic per month

\* Enterprise Plan: custom pricing



Estimated monthly cost for 1,000 patient interactions:



\* AI cost: about $3

\* Server cost: about $10

\* Total cost: about $13



\---



\## Target Audience



The target audience is small and medium clinics, especially:



\* Dental clinics

\* Family medicine clinics

\* Pediatric clinics

\* Dermatology clinics

\* Cardiology clinics



The first version focuses on Palestinian cities:



\* Nablus

\* Hebron

\* Ramallah

\* Jenin

\* Bethlehem



\---



\## Safety Note



Smart Clinic AI Agent does not replace doctors and does not provide medical diagnosis.



For life-threatening symptoms, patients should contact local emergency services immediately.



\---



\## Final Project Requirements Covered



This project includes:



\* Working AI Agent

\* CrewAI implementation

\* Role, goal, and backstory

\* Multiple tools

\* RAG

\* Skills

\* Evals

\* Streamlit demo

\* Business plan

\* Pitch script

\* Presentation content

\* README

\* `.env.example`

\* Organized project folder



