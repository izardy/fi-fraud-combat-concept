# Combat Fraud and Scam
## A Framework Conceptualization
### Problem Statement
- Issues highlighted in the existing process
    - Issue 1 : Scam/Fraud/Mule Account activities reported only after it happened
    - Issue 2 : Lack of preventive measure i.e near real time monitoring on the latest scam informations for FI
    - Issue 3 : FI only have latest updated records of scam/fraud information from governing institutions. 
    - Issue 4 : No direct information sharing real-time event platform from other FI. 
### Propose Conceptual Solution
- Based on the issues highlighted and performed gap analysis, a sandbox is proposed to demonstrate how the above might be able to counter.
  #### Establish a database which combined data of suspected mule/fraud/scam accounts from 3 different sources
    - [ ] **Rule based approach** to be implemented at first layer (Source no.1)
        - [ ] Existing rule based approach (i.e changes of email, too many transaction in a day, student/housewife status but have continuous multiple transaction in a day)
        - [ ] SQL query suspected accounts based on the above logic/rule
        - [ ] Ingest into scam/fraud/mule centralise database
    - [ ] **ML based approach** to be implemented at second layer (Source no.2)
        - [ ] Obtain data
        - [ ] Build ML model
        - [ ] Train ML model
        - [ ] Test ML model
        - [ ] Deploy ML model
        - [ ] Ingest into scam/fraud/mule centralise database
    - [ ] **Public shared approach** to be implemented at third layer (Source no.3)
        - [ ] Identify platforms where public can share scam information
        - [ ] Prepare data entry platform
        - [ ] Manual data entry for this info
        - [ ] Ingest into scam/fraud/mule centralise database
  #### Monitoring suspected accounts
     - [ ] Validation process
         - [ ] Flag confirmed/suspected 
     - [ ] API sharing
         - [ ] Internally
         - [ ] Externally 
  #### Actions        
     - [ ] Notification alert
        - [ ] Internally
        - [ ] Externally 
                
### System Architecture : TOGAF BDAT Approach

| No. |Business Logic| Data Source | Application Use | Technology Use  |
--|------------|-------------|-----------------|-----------------|
|1|Continuous check at account level on CIF updates i.e email address and sub-sequent activities after the update.| CBS | | Linux Server, Python3, Bash, Cron |
|2|To notify and confirm with clients on suspicious activities via SMS/Whatsapp/Phone Call.|CBS| | Linux Server, Python3, Bash, Cron |
|3|Implementation of rule based approach upon transaction initialisation. | CBS| | Linux Server, Python3, Bash, Cron|
|4|Implementation of ML based approach upon transaction initialisation. | CBS| AWS SageMaker  | Scikit-Learn, Linux Server, Python3, Bash, Cron |
|5|Notifications | Data created upon No.2 & 3 activities initiate | Whatsapp Web| Selenium, Ollama, Linux Server, Nvidia Cuda |
|6|Scrape scam/fraud/mule acount from various sources & publish data in a platform, enable API and new data additional | Open source data| OSINT Platform | Linux Server, Python3, Bash, Cron, Cloudflare, Solr|

### Using This Repo
- Environment preparation
  #### Installation
     - [ ] Install Python3.10
     - [ ] Create env either by conda or pyenv
     - [ ] ```conda active env``` or ```source env\path\bin```
     - [ ] ```git clone git@github.com:izardy/fi-fraud-combat-concept.git```
     - [ ] ```cd fi-fraud-combat-concept```
     - [ ] ```pip install -r requirements.txt```
  #### Test Scam/Fraud Public Sharing Platform Approach
     - [ ] ```flask --app flaskr run --debug```
     - [ ] Check https://localhost:5000 to access the web apps
     - [ ] All the shared data ingested into sqlite db via method3_public_contribution/instance/flaskr.sqlite (table name scammers)
  #### Test ML 
     - [ ] ```cd method2_machine_learning```
     - [ ] ```python predict.py```
     - [ ] The code will run and predict suspected fraud account using sample data as input
     - [ ] Data of the fraud account ingested into sqlite db via method3_public_contribution/instance/flaskr.sqlite (table name scammers)
  #### Test Rule Based 
     - [ ] Based on dummy CIF and transaction data , we extract account information which  had changes in their email address 
     - [ ] ```python rule-based.py```
     - [ ] The code will run and filter account based on the applied rule
     - [ ] Output data ingested into sqlite db via method3_public_contribution/instance/flaskr.sqlite (table name scammers)
 
  ### Pull the Combined Data via API
    - [ ] User need to login into the Flask app before can use the API
    - [ ] https://localhost:5000/api/scammers
           
     
