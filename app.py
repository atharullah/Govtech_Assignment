import os
import pandas as pd
import dateutil.parser

def data_cleaning_and_validation(df,clean_path):
    #Cleaning#

    # Remove any rows which do not have a name field (treat this as unsuccessful applications)
    unssuccessfull_df=df[df['name'].isnull()]
    df = df.dropna(subset=['name'])
    # Split name into first_name and last_name
    df[["first_name", "last_name"]]=df['name'].replace(['Miss ','Mr\. ','Ms\. ','Dr\. ','Mrs\. '],'', regex=True).str.split(' ', expand=True).iloc[:, :2]
    df=df.drop("name",axis=1)
    # Format birthday field into YYYYMMDD
    df["date_of_birth"]=pd.to_datetime(df['date_of_birth'], infer_datetime_format=True).dt.strftime('%Y%m%d')

    #Validation#
    # Check if mobile number is 8 digits
    df = df[df['mobile_no'].astype(str).str.len() == 8]
    # Check if applicant is over 18 years old as of 1 Jan 2022
    df['above_18'] = pd.to_datetime(df['date_of_birth']).apply(lambda x: (pd.Timestamp('2022-01-01') - x).days // 365 >= 18)
    df = df[df['above_18']]
    # Check if applicant has a valid email
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    df = df[df['email'].str.contains(email_pattern)]
    print(df)
    

if __name__ == "__main__":
    # Data Ingestion
    input_folder = 'input/'
    clean_folder = 'cleaned/'
    for filename in os.listdir(input_folder):
        if filename.startswith('applications_') and filename.endswith('.csv'):
            input_path = os.path.join(input_folder, filename)
            clean_path = os.path.join(clean_folder, filename)
            df = pd.read_csv(input_path)
            data_cleaning_and_validation(df,clean_path)