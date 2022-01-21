###process for registering new patient. 

#find element by link text: New COVID-19 vaccination patient
#send keys to id=patient_firstName
#send keys to id=patient_lastName
#send keys to id=patient_dateOfBirth
#medicare id = patient_typeOfIdProvided
#click yes or no 
#medicare id = patient_medicareNumber
#medi ref = patient_medicareReferenceNumber
#next button : button_step_1
#consent: id = patient_reportConsent_yes
#finish: finish_btn
#add encounter: 
#<a href="/vaccination-records/new?pid=6700923" class="btn btn-secondary add_vax_patient_list_btn" style="">Add Vaccination Encounter</a>

###add encounter: 
#vax given: light_vax_vaxGiven_0
# 3rd dose: light_vax_doseInfo_3
#vaccine type: light_vax_vaccineType
# astra: <option value="AstraZeneca">AstraZeneca</option>
#pfizer: <option value="Pfizer (Comirnaty)">Pfizer (Comirnaty)</option>
# date and time id: light_vax_administration_date_date
#light_vax_administration_date_time_hour ->>> hour id
#minute id = : light_vax_administration_date_time_minute
# save id = submitbutton


