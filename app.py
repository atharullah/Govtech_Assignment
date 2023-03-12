import os
import pandas as pd
import dateutil.parser

def data_cleaning(df):
    # name column cleaning and spliting
    df[["first_name", "last_name"]]=df['name'].replace(['Miss ','Mr\. ','Ms\. ','Dr\. ','Mrs\. '],'', regex=True).str.split(' ', expand=True).iloc[:, :2]
    df=df.drop("name",axis=1)

    #format dob
    df["date_of_birth"]=pd.to_datetime(df['date_of_birth'], infer_datetime_format=True).dt.strftime('%Y%m%d')
    
    print(df)
  

if __name__ == "__main__":
    # Data Ingestion
    input_folder = 'input/'
    output_folder = 'cleaned/'
    for filename in os.listdir(input_folder):
        if filename.startswith('applications_') and filename.endswith('.csv'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            df = pd.read_csv(input_path)
            data_cleaning(df)