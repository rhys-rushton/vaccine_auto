class Patient():
    def __init__(self,name, surname, DOB, gender, medicare, address, suburb, post_code, date, vax_type, error = ''):
        self.name = name
        self.suranme = surname
        self.DOB = DOB
        self.gender = gender
        self.medicare = medicare
        self.address = address
        self.suburb = suburb 
        self.post_code = post_code
        self.date = date
        self.vax_type= vax_type
        self.error = error

        