## Automation Tool for Uploading Vaccine Data for COVID-19 (AUSTRALIA)
This is a python CLI script for automating the upload of vaccination information for those who are receiving their booster shot. 
In order to use this app. you will need to be a registered user on the government respiratory clinic app. and you will also need access to the relevant patient
management system for sourcing data. The two data sources I have been using is Aspen Medical's Rhino app and Zedmed. 
This script will upload the details of those who are not yet registered on the database, and for those who are registered it will add their booster dose. Furthermore, there is a
file for checking if a there are any potential duplicate patients. 

## Table of Contents 
- [How to Run and Install](#how-to-run-and-install)
- [Registering Patients and Adding Encounters](#registering-patients-and-adding-encounters)
- [Find Duplicates](#finding-duplicates)
- [Dependencies](#dependencies)

## How to Run and Install
This autmation tool requires you to have [Python](https://www.python.org/) installed. You will also need a wedriver for whatever browser it is that you are using. 
You will also need to install some dependenices. 

```sh
pip install pandas
pip install selenium
```
The inputs and outputs are configured to be specific to a certain computer, these will need to be changed if you move location. 

Put the relevant data folders into the '.\csv_operations\data'

All csv files are never uploaded to github because of data sensitivity. 

