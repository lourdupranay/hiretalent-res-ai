A Python program that matches job descriptions with preprocessed resumes by leveraging semantic embeddings and cosine similarity. This program preprocesses both job descriptions and resumes, generates embeddings using spaCy, calculates similarity scores, and ranks the resumes based on their relevance to the job description.

How to use this program in VSCode ?

1. Checkout this Program
2. Open terminal in VSCode 
3. Create a Python Virtual environment 
   python -m venv resumeenv
4. Activate Python virtual environment
   /resumeenv/Scripts/activate
5. Install dependencies
   python install -r requirements.txt
6. Install spacy model used in the program
   python -m spacy download en_core_web_sm
7. Start the program
   cd src
   python .\recruitwise-api.py
8. Program will start running on
    * Running on all addresses (0.0.0.0)
    * Running on http://127.0.0.1:5000
    * Running on http://192.168.29.2:5000
9. Open one more terminal
10. API Request format

Testing with training data ------
API Request for Training Data Category resume ----
Invoke-WebRequest -Method Post -Uri 'http://127.0.0.1:5000/match' -Headers @{ "Content-Type" = "application/json" } -Body '{"context": "sap professional 7 years experience", "category": "resume", "threshold": "0.7", "noOfMatches": 3, "inputPath": "https://console.cloud.google.com/storage/browser/hackathon1415"}'

API Request for Training Data Category job ----
Invoke-WebRequest -Method Post -Uri 'http://127.0.0.1:5000/match' -Headers @{ "Content-Type" = "application/json" } -Body '{"context": "Lead Software Engineer", "category": "job", "threshold": "0.7", "noOfMatches": 3, "inputPath": "https://console.cloud.google.com/storage/browser/hackathon1415"}'


Testing with actual test data ------
API Request for test Data Category resume ----
Invoke-WebRequest -Method Post -Uri 'http://127.0.0.1:5000/match' -Headers @{ "Content-Type" = "application/json" } -Body '{"context": "Media Activities Specialist", "category": "resume", "threshold": "0.7", "noOfMatches": 3, "inputPath": "https://console.cloud.google.com/storage/browser/hackathontestdata2024"}'


API Request for test Data Category job ----
Invoke-WebRequest -Method Post -Uri 'http://127.0.0.1:5000/match' -Headers @{ "Content-Type" = "application/json" } -Body '{"context": "Media Activities Specialist", "category": "job", "threshold": "0.7", "noOfMatches": 3, "inputPath": "https://console.cloud.google.com/storage/browser/hackathontestdata2024"}'

11. Example API execution and result -  open new terminal. As this will Powershell. below examples are for Powershell.
    * Resume Recommendation API - Category - resume
   Sample Request - 
   Invoke-WebRequest -Method Post -Uri 'http://127.0.0.1:5000/match' -Headers @{ "Content-Type" = "application/json" } -Body '{"context": "Java J2EE developer 5 years experience", "category": "resume", "threshold": "0.7", "noOfMatches": 3, "inputPath": "https://console.cloud.google.com/storage/browser/hackathon1415"}'
   Sample Response - 
   Resumes Directory is having huge set of resumes. Enable limit flag in fetch_test_data.py line no. 32 to 35 and then run the program.

   * Job Recommendation API - Category -job
   Program will generate jobs directory and fetch all the job descriptions placed at 
   https://console.cloud.google.com/storage/browser/hackathon1415/JD/

   Sample Request - 
   Invoke-WebRequest -Method Post -Uri 'http://127.0.0.1:5000/match' -Headers @{ "Content-Type" = "application/json" } -Body '{"context": "Java J2EE developer 5 years experience", "category": "job", "threshold": "0.4", "noOfMatches": 3, "inputPath": "https://console.cloud.google.com/storage/browser/hackathon1415"}'
   
   Sample Response - 
   {
    "count": 3,
    "metadata": {
        "confidenceScore": 0.4
    },
    "results": [
        {
            "id": "Lead Information Security Engineer - Web-based Applications Security-R-316166.docx",
            "score": 0.6426610946655273
        },
        {
            "id": "Senior Software Engineer - Hybris-Payments Domain",
            "score": 0.6202497482299805
        },
        {
            "id": "Senior Software Engineer - Hybris-Payments Domain",
            "score": 0.6171873807907104
        }
    ]
}





    
