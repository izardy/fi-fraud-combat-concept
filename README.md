# BIMB Hacktive
## Fraud Detection System : A Framework Conceptualization
### Problem Statement
- Issues highlighted in the existing process
    - Issue 1 : Scam/Fraud/Mule Account activities reported only after it happened
    - Issue 2 : No preventive measure. Whereby notifcation in term of email to customers & bank
    - Issue 3 : Bank only have latest updated records of scam/fraud information from PDRM. 
    - Issue 4 : No direct information sharing real-time event platform from other FI. 

### Propose Conceptual Solution
- Based on the issues highlighted, we want to built a sandbox to demonstrate how the above might be able to counter.
    - Issue 1 & 2
        - *On situation where mule account about to be created*
            - [ ] *Continuous check at account level on CIF updates i.e email address and sub-sequent activities after the update.*
            - [ ] *To notify and confirm with clients on suspicious activities via SMS/Whatsapp/Phone Call*
        - *On situation where potential scam/fraud victiom to initiate money transfer*
            - [ ] *Rule based approach to be implemented at first layer*
            - [ ] *ML based approach to be implemented at second layer*
            - [ ] *Notification within the apps*
            - [ ] *Notification at customer phone number*
            - [ ] *Notification to bank on this alert*

    - Issue 2 & 3
        - *To establish a repository where scam/fraud/mule account 

### System Architecture : TOGAF BDAT Approach

| No. |Business Logic| Data Source | Application Use | Technology Use  |
--|------------|-------------|-----------------|-----------------|
|1|Continuous check at account level on CIF updates i.e email address and sub-sequent activities after the update.| CBS | | Linux Server, Python3, Bash, Cron |
|2|To notify and confirm with clients on suspicious activities via SMS/Whatsapp/Phone Call.|CBS| | Linux Server, Python3, Bash, Cron |
|3|Implementation of rule based approach upon transaction initialisation. | CBS|  Linux Server, Python3, Bash, Cron|
|4|Implementation of ML based approach upon transaction initialisation. | CBS|  | Scikit-Learn, Linux Server, Python3, Bash, Cron |
|5|Notifications | Data created upon No.2 & 3 activities initiate | Whatsapp Web| Selenium, Ollama, Linux Server, Nvidia Cuda |
