import os
import pandas as pd
import hashlib

def data_cleaning_and_validation():
    # Data Ingestion
    input_folder = '../data/input/'
    success_folder = '../data/success/'
    failed_folder = '../data/failed/'
    for filename in os.listdir(input_folder):
        if filename.startswith('applications_') and filename.endswith('.csv'):
            input_path = os.path.join(input_folder, filename)
            success_path = os.path.join(success_folder, filename)
            failed_path = os.path.join(failed_folder, filename)
            df = pd.read_csv(input_path)
            # Remove any rows which do not have a name field (treat this as unsuccessful applications)
            failed_df=df[df['name'].isnull()]
            df = df.dropna(subset=['name'])
            # Split name into first_name and last_name
            df[["first_name", "last_name"]]=df['name'].replace(['Miss ','Mr\. ','Ms\. ','Dr\. ','Mrs\. '],'', regex=True).str.split(' ', expand=True).iloc[:, :2]
            df=df.drop("name",axis=1)

            # Format birthday field into YYYYMMDD
            df["date_of_birth"]=pd.to_datetime(df['date_of_birth'], infer_datetime_format=True).dt.strftime('%Y%m%d')

            # Create above_18 column to check if applicant is over 18 years old as of 1 Jan 2022
            df['above_18'] = pd.to_datetime(df['date_of_birth']).apply(lambda x: (pd.Timestamp('2022-01-01') - x).days // 365 >= 18)
            df['above_18'] = df['above_18'].astype(bool)

            # Check if mobile number is 8 digits
            failed_df=pd.concat([failed_df,df[df['mobile_no'].astype(str).str.len() != 8]])
            df = df[df['mobile_no'].astype(str).str.len() == 8]

            # Check if applicant is over 18 years old as of 1 Jan 2022
            failed_df=pd.concat([failed_df,df[~df['above_18']]])
            df = df[df['above_18']]

            # Check if applicant has a valid email
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            failed_df=pd.concat([failed_df,df[~df['email'].str.contains(email_pattern)]])
            df = df[df['email'].str.contains(email_pattern)]

            df['membership_id'] = df.apply(lambda row: f"{row['last_name']}_{hashlib.sha256(row['date_of_birth'].encode('utf-8')).hexdigest()[:5]}", axis=1)
            df.to_csv(success_path, index=False)

            failed_df.to_csv(failed_path, index=False)
            df.to_csv(success_path, index=False)

if __name__=="__main__":
    data_cleaning_and_validation()