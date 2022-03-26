import pandas as pd 
import numpy as np 
from datetime import datetime
import numpy as np
import warnings
warnings.filterwarnings("ignore")




adult= pd.read_excel("data_adults_additional_data.xlsx")





def years_between(d1, d2): # get differences in years 
    d1 = d1
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    diff_days = abs((d2 - d1).days)
    return  np.round((diff_days/365),1)

if __name__ == "__main__":
    print
    
    adult= adult.rename(columns={"lisibility": "quality","individual":"subject"})    #rename columns
    adult_pre_procdessed = adult[["subject","gender","age","speed","quality"]] # select relevant cols
    adult_pre_procdessed["age"]=adult_pre_procdessed["age"].apply(lambda x: years_between(x,"2022-02-02")) # adjust age to right format
    ## here improvemend is needed since we need to take the difference between birth date and test date
    adult_pre_procdessed["gender"]= adult_pre_procdessed.gender.replace("boy",0).replace("girl",1)  # change boy, girls notation
    adult_pre_procdessed.to_csv("adult_pre_procdessed_meta_data.csv")
    print("adult data pre-processed and saved as a csv. : adult_pre_procdessed_meta_data.csv")
