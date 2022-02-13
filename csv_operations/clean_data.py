import pandas as pd
import glob

#we need to import vaccine data for both pfizer and astra
#we need to merge the vaccine data for pfizer and astra
#we want to drop duplicates based on the date upon which they were last in and their file number. 
pd.set_option('display.float_format', lambda x: '%.0f' % x)
dsp_data = pd.read_csv(r'H:\vaccine_auto\csv_operations\data\dsp\DSPatients.csv', header=0, encoding='CP1252')

fields_to_drop = ['CLINIC_CODE_x', 'TITLE_x','MAILING_ADDRESS_LINE_1_x',
       'MAILING_ADDRESS_LINE_2_x', 'MAILING_SUBURB_TOWN_x',
       'MAILING_POSTCODE_x', 'MOBILE_PHONE', 'patient_name', 'full_name',
       'full_suburb', 'address', 'full_mailing_suburb', 'TITLE_y',
       'FAMILY_NAME_y', 'GIVEN_NAME_y', 'HOME_ADDRESS_LINE_1_y',
       'HOME_ADDRESS_LINE_2_y', 'HOME_SUBURB_TOWN_y', 'HOME_POSTCODE_y',
       'HOME_PHONE_y','AGE_y', 'GENDER_y', 'USUAL_CLINIC',
       'USUAL_DOCTOR', 'TYPE_CODE', 'STATUS_CODE',
       'PRACTICE_DEFINABLE_FIELD1_CODE', 'PRACTICE_DEFINABLE_FIELD2_CODE',
       'PRACTICE_DEFINABLE_FIELD3_CODE', 'PRACTICE_DEFINABLE_FIELD4_CODE',
       'PRACTICE_DEFINABLE_FIELD5_CODE', 'PRACTICE_DEFINABLE_FIELD6',
       'PRACTICE_DEFINABLE_FIELD7', 'PRACTICE_DEFINABLE_FIELD8',
       'PRACTICE_DEFINABLE_FIELD9', 'PRACTICE_DEFINABLE_FIELD10', 'FIRST_IN',
       'LAST_IN_y', 'ALERTS', 'CLINIC_CODE_y', 'MAILING_SUBURB_TOWN_y', 'MAILING_POSTCODE_y', 'FAMILY_ID','VETERAN_AFFAIRS_NUMBER',
       'VETERAN_FILE_NUMBER_EXPIRY_DATE', 'PATIENT_HEALTH_CARE_CARD',
       'PATIENT_HLTH_CARE_CARD_EX_DATE', 'SAFETY_NET_NO']


vax_choice = input('Are you doing pfizer (p) or astra (a)?')

if vax_choice == 'a':
    path = r'H:\vaccine_auto\csv_operations\data\astra'
    vax_type = 'astra'
    print('Astra')

elif vax_choice == 'p':
    print('Pfizer')
    path = r'H:\vaccine_auto\csv_operations\data\pfizer'
    vax_type = 'pfizer'
else:
    print('Error with vax data clean')
    



#this is where we merge the socialble/unsocialble billing hours. 
#returns merged dataframes
def item_number_to_df (path):
    data_list = []
    data_filenames = glob.glob(path + "\*.csv")

    for csv in data_filenames: 
        df = pd.read_csv(csv,index_col=None, header=0, encoding ='CP1252')
        data_list.append(df)

    data_frame = pd.concat(data_list, axis=0,ignore_index=True)
    merged_data = pd.merge(data_frame,dsp_data, on= 'FILE_NUMBER', how = 'inner')
    merged_data.drop(fields_to_drop, axis = 1, inplace = True)
    merged_data.MEDICARE_NUMBER = merged_data.MEDICARE_NUMBER.astype(str)
    merged_data.HOME_POSTCODE_x = merged_data.HOME_POSTCODE_x.astype(str)
    merged_data = merged_data.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    merged_data['MEDICARE_NUMBER'] = merged_data['MEDICARE_NUMBER'].str.replace('.0', '', regex=False)
    merged_data['MEDICARE_NUMBER'] = merged_data['MEDICARE_NUMBER'].str.replace('_', '', regex=False)
    merged_data['MEDICARE_NUMBER'] = merged_data['MEDICARE_NUMBER'].str.strip()
    merged_data.drop_duplicates(subset=['FILE_NUMBER', 'LAST_IN_x'])
    merged_data['vax_type'] = vax_type
    merged_data['auto_outcome'] = ''
    return merged_data


vaccine_data = item_number_to_df(path)
#print(vaccine_data['MEDICARE_NUMBER'])
#for col in vaccine_data.columns: 
    #print(col)
vaccine_data = (vaccine_data.transpose()).to_dict()
#print(vaccine_data)




fields = ['FILE_NUMBER',
'FAMILY_NAME_x',
'GIVEN_NAME_x',
'HOME_ADDRESS_LINE_1_x',
'HOME_ADDRESS_LINE_2_x',
'HOME_SUBURB_TOWN_x', 
'HOME_POSTCODE_x', 
'HOME_PHONE_x',
'AGE_x',
'GENDER_x',
'LAST_IN_x',
'DATE_OF_BIRTH',
'PATIENT_ID',
'MAILING_ADDRESS_LINE_1_y',
'MAILING_ADDRESS_LINE_2_y',
'MEDICARE_NUMBER',
'MEDICARE_BASE_NUMBER',
'MEDICARE_NUMBER_EXPIRY',
'email_ADDRESS',
'vax_type', 
'auto_outcome'] 


##clean data for checking for vaccination duplicates. 
#rhino_df = pd.read_csv(r'H:\vaccine_auto\csv_operations\data\rhino\Blacktown 2022-01-31 02.11 Vaccinations.csv')
#rhino_data_dup_check = (rhino_df.transpose()).to_dict()

