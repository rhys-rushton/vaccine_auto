from functions.login import login
from csv_operations.clean_data import rhino_data_dup_check as data_to_use
import csv

possible_duplicates = []
dupe_error = []

fields = ['clinic_id','clinic_name','first_name','last_name','patient_display_id','date_of_birth','gender','indigenous_status','medicare_number','address_line1','address_line2','suburb','state','postcode','phone_number','mobile_number','emergency_contact_name','emergency_contact_phone','country_of_birth','home_language','vaccine_given','dose','vaccine_brand','administration_date','administration_time' ]

def main ():
    print('hey')
    driver = login()

    for key in data_to_use: 
        #if key > 100: 
            #break
        try: 
            driver.get("https://app.respiratoryclinic.com.au/dashboard/")
            name = data_to_use[key]['first_name']
            last_name = data_to_use[key]['last_name']

            existing_vax_patient = driver.find_element_by_link_text('Existing Vaccination Patients')
            existing_vax_patient.click()

            given_name_field = driver.find_element_by_id('firstName')
            last_name_field = driver.find_element_by_id('lastName')

            given_name_field.send_keys(name)
            last_name_field.send_keys(last_name)

            search_button = driver.find_element_by_class_name('btn.btn-dark')
            search_button.click()

        except Exception as e:
            dupe_error.append(data_to_use[key])
            print(e)
            continue



        try: 
            assert driver.find_element_by_xpath("//*[contains(text(), 'Potential Duplicate found')]").is_displayed()
            possible_duplicates.append(data_to_use[key])
            print('duplicate')

        except:
            print('No duplicate')
            
    print('done')
    
main()

with open(r'H:\vaccine_auto\output\duplicates.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(dupe_error)


with open(r'H:\vaccine_auto\output\duplicates.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(possible_duplicates)