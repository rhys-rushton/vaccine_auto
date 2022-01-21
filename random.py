









''' 

    #data is the big data frame. 
    data = pd.concat(li, axis =0, ignore_index=True)
    
    #print(data)

elif int(data_source) == 2:
    print("hey this is where we do astra zeneca")
vax_type = 'A'
def make_dictionary_to_return (vaccine_data_source) :
    #now we need to add the patients date of birth. 
    #do this by going through DSP file and comparing file numbers. 
    # r'C:\Users\RRushton\Desktop\vaccineboosterautomation\csv_operations\DSPatients.csv'
    # r'H:\vaccineboosterautomation\csv_operations\csv_data\DSPatients.csv'
    dsp_data = pd.read_csv(r'H:\vaccineboosterautomation\csv_operations\csv_data\DSPatients.csv', header=0, encoding ='CP1252')
    #dsp_data.set_index("FILE_NUMBER", inplace=True)
    #print(dsp_data)
    #vaccine_data_source.set_index("FILE_NUMBER", inplace=True)
    #print(vaccine_data_source)

    transposed_dict_dsp = dsp_data.transpose().to_dict()
    vaccine_data_dict = vaccine_data_source.transpose().to_dict()

    #print(transposed_dict_dsp)
    #print(vaccine_data_dict)
    count = 0
    for key in transposed_dict_dsp:
        if key in vaccine_data_dict.keys():
            data_to_return[count] = transposed_dict_dsp[key]
            #need to use dict.pop()
            count += 1
    
    #at the end of the function return the data. 
    return data_to_return
make_dictionary_to_return(data)
'''
