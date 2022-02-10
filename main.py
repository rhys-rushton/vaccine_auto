from dataclasses import fields
from random import randrange
from sys import excepthook
from classes import patient
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time 
import csv
from csv_operations import clean_data
import traceback
from functions.login import login
from csv_operations import clean_data
from functions.look_for_date import look_for_date, find_date_click
from functions.date_string import remove_zeroes

#vaccination_data
patient_data = clean_data.vaccine_data
csv_fields = clean_data.fields 

patient_rego_success = []
patient_rego_error = []
patient_vax_succ = []
patient_vax_err = []
patient_vax_prexisting = []


def add_encounter(patient_object, driver):
    try: 
        print('adding encounter')
        vax_given = driver.find_element_by_id('light_vax_vaxGiven_0')
        vax_given.click()
        third_dose = driver.find_element_by_id('light_vax_doseInfo_3')
        third_dose.click()

        time.sleep(0.5)
        vax_type = Select(driver.find_element_by_id('light_vax_vaccineType'))
        print(patient_object.vax_type)

        if patient_object.vax_type == 'pfizer':
            vax_type = Select(driver.find_element_by_id('light_vax_vaccineType'))
            vax_type.select_by_visible_text('Pfizer (Comirnaty)')
        elif patient_object.vax_type == 'astra':
            vax_type = Select(driver.find_element_by_id('light_vax_vaccineType'))
            vax_type.select_by_visible_text('AstraZeneca')
        
        date_of_encounter = driver.find_element_by_id('light_vax_administration_date_date')
        date = remove_zeroes(patient_object.date)
        date_of_encounter.clear()
        date_of_encounter.send_keys(date)

        hour = Select(driver.find_element_by_id('light_vax_administration_date_time_hour'))
        minute = Select(driver.find_element_by_id('light_vax_administration_date_time_minute'))

        rand_hour = randrange(9,19)
        rand_min = randrange(0, 59)

        hour.select_by_value(str(rand_hour))
        minute.select_by_value(str(rand_min))
        time.sleep(0.5)

        
        save_button = driver.find_element_by_id('submitbutton')
        save_button.click()

        time.sleep(0.5)
    except Exception as e:
        print(e)
        time.sleep(0.5)
        print('error in add vax')

    url = driver.current_url

    try:
        assert url == 'https://app.respiratoryclinic.com.au/dashboard/'
        print('encounter success')
        patient_vax_succ.append(patient_object)
    except Exception as e:
        print('error in add vax')
        print(e)
        driver.get('https://app.respiratoryclinic.com.au/dashboard/')
        patient_vax_err.append(patient_object)

    time.sleep(0.5)







def check_patient_exists(patient_object, driver):
    print('checking patient exists')
    existing_patient_button = driver.find_element_by_link_text('Existing Vaccination Patients')
    existing_patient_button.click()
    first_name_input = driver.find_element_by_id('firstName')
    last_name_input = driver.find_element_by_id('lastName')
    first_name_input.send_keys(patient_object.name)
    last_name_input.send_keys(patient_object.surname)
    search_button = driver.find_element_by_class_name('btn.btn-dark')
    search_button.click()

    try:
        driver.find_element_by_xpath("//*[contains(text(), 'No results.')]").is_displayed()
        driver.get("https://app.respiratoryclinic.com.au/dashboard/")
        return False

    except:
        print('Hey')
        date_of_birth = remove_zeroes(patient_object.DOB)
        date_of_birth_present = look_for_date(date_of_birth, driver)

        if date_of_birth_present == True:
            encounter_date = remove_zeroes(patient_object.date)
            encounter_date_present = look_for_date(encounter_date, driver)

            if encounter_date_present == True:
                patient_vax_prexisting.append(patient_object)
                print('Patient Already Registered and done')
                return True
            else:
                try:
                    find_date_click(date_of_birth, driver)
                    print('find date click')
                    time.sleep(0.5)
                except:
                    patient_vax_err.append(patient_object)
                    return False
                
                try: 
                    
                    #add the encounter
                    print('add encoutner after find date click')
                    time.sleep(0.5)
                    add_encounter(patient_object,driver)
                    print('add encoutner after find date click')
                    time.sleep(0.5)
                    #patient_vax_succ.append(patient_object)
                    return True
                except: 
                    #patient_vax_err.append(patient_object)
                    return True
        else:
            #patient doesn't exist. 
            driver.get("https://app.respiratoryclinic.com.au/dashboard/")
            return False









def register_patient(patient_object, driver):
    print('we are registering a new patient')

    try:
        new_patient_button = driver.find_element_by_link_text("New COVID-19 vaccination patient")
        new_patient_button.click()
    except Exception as e:
        print(e)
        patient_rego_error.append(patient_object)

    try:
        first_name = driver.find_element_by_id('patient_firstName')
        last_name = driver.find_element_by_id('patient_lastName')
        dob = driver.find_element_by_id('patient_dateOfBirth')

        first_name.send_keys(patient_object.name)
        last_name.send_keys(patient_object.surname)
        dob.send_keys(remove_zeroes(patient_object.DOB))
        try:
            medicare_field = Select(driver.find_element_by_id('patient_typeOfIdProvided'))
            if patient_object.medicare == '':
                medicare_field.select_by_visible_text('No - Other ID sighted')
            elif patient_object.medicare != '':
                medicare_field.select_by_visible_text('Yes - Medicare Card')
                patient_medicare_num = driver.find_element_by_id('patient_medicareNumber')
                patient_medicare_ref = driver.find_element_by_id('patient_medicareReferenceNumber')
                patient_medicare_ref.send_keys(patient_object.medicare[10])
                patient_medicare_num.send_keys(patient_object.medicare[0:10])
        except Exception as e:
            if  'string index out of range' in e.args:
                medicare_field.select_by_visible_text('No - Other ID sighted')

            

        time.sleep(0.5)
        next_button = driver.find_element_by_id('button_step_1')
        next_button.click()
        time.sleep(0.5)

        driver.find_element_by_id('patient_reportConsent_yes').click()
        driver.find_element_by_id('finish_btn').click()
        
        url = driver.current_url
        if url != 'https://app.respiratoryclinic.com.au/dashboard/':
            driver.find_element_by_id('finish_btn').click()
        patient_rego_success.append(patient_object)
        time.sleep(0.5)
        driver.find_element_by_link_text('Add Vaccination Encounter').click()

        add_encounter(patient_object, driver)
        

    except Exception as e:
        print('reigstration error')
        print(e)
        time.sleep(0.5)
        patient_rego_error.append(patient_object)





def vaccinate_main():

    print('We are now uploading new patients.')
    driver = login()

    #need to iterate through imported dictionary. 
    for key in patient_data:

        #get rid of this. 
        #if key > 100:
            #print('Breaking')
            #break

        url = driver.current_url
        try: 
            print('Correct URL')
            assert url == "https://app.respiratoryclinic.com.au/dashboard/"
        except:
            driver.get('https://app.respiratoryclinic.com.au/dashboard/')

        given_name = patient_data[key]['GIVEN_NAME_x']
        surname = patient_data[key]['FAMILY_NAME_x']
        date_of_birth = patient_data[key]['DATE_OF_BIRTH']
        gender = patient_data[key]['GENDER_x']
        medicare = patient_data[key]['MEDICARE_NUMBER']
        address = patient_data[key]['HOME_ADDRESS_LINE_1_x']
        suburb = patient_data[key]['HOME_SUBURB_TOWN_x']
        postcode = patient_data[key]['HOME_POSTCODE_x']
        encounter_date = patient_data[key]['LAST_IN_x'][0:10]
        vax_type = patient_data[key]['vax_type']
        error = ''
        patient_object = patient.Patient(given_name, surname, date_of_birth, gender, medicare, address, suburb, postcode, encounter_date, vax_type, error)

        #now check if the patient exists or not. 
        patient_exists = check_patient_exists(patient_object, driver)

        if patient_exists == False:
            print('Patient doesnt exist')
            register_patient(patient_object, driver)
            continue
        elif patient_exists == True: 
            print('Patient is already done')
            continue


vaccinate_main()


#patient registration success csv
with open(r'H:\vaccine_auto\output\rego_succ.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([csv_fields])
    for patient_obj in patient_rego_success:
        writer.writerow([patient_obj.name, patient_obj.surname, patient_obj.DOB, patient_obj.gender, patient_obj.medicare, patient_obj.address, patient_obj.suburb, patient_obj.post_code, patient_obj.date, patient_obj.vax_type, patient_obj.error])

#patient registration error csv
with open(r'H:\vaccine_auto\output\rego_err.csv', 'w',newline='' ) as f:
    writer = csv.writer(f)
    writer.writerow([csv_fields])
    for patient_obj in patient_rego_error:
        writer.writerow([patient_obj.name, patient_obj.surname, patient_obj.DOB, patient_obj.gender, patient_obj.medicare, patient_obj.address, patient_obj.suburb, patient_obj.post_code, patient_obj.date, patient_obj.vax_type, patient_obj.error])

#vax upload success
with open(r'H:\vaccine_auto\output\vax_upload_succ.csv', 'w',newline='') as f:
    writer = csv.writer(f)
    writer.writerow([csv_fields])
    for patient_obj in patient_vax_succ:
        writer.writerow([patient_obj.name, patient_obj.surname, patient_obj.DOB, patient_obj.gender, patient_obj.medicare, patient_obj.address, patient_obj.suburb, patient_obj.post_code, patient_obj.date, patient_obj.vax_type, patient_obj.error])

#vax upload error
with open(r'H:\vaccine_auto\output\vax_upload_err.csv', 'w',newline='') as f:
    writer = csv.writer(f)
    writer.writerow([csv_fields])
    for patient_obj in patient_vax_err:
        writer.writerow([patient_obj.name, patient_obj.surname, patient_obj.DOB, patient_obj.gender, patient_obj.medicare, patient_obj.address, patient_obj.suburb, patient_obj.post_code, patient_obj.date, patient_obj.vax_type, patient_obj.error])

#vaxes already done
with open(r'H:\vaccine_auto\output\already_done.csv', 'w',newline='') as f:
    writer = csv.writer(f)
    writer.writerow([csv_fields])
    for patient_obj in patient_vax_prexisting:
        writer.writerow([patient_obj.name, patient_obj.surname, patient_obj.DOB, patient_obj.gender, patient_obj.medicare, patient_obj.address, patient_obj.suburb, patient_obj.post_code, patient_obj.date, patient_obj.vax_type, patient_obj.error])





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


