# Solution Details

This contains diffrent folders as per the requirement

## Prerequisites

- Python 3.6 or higher
- pandas, hashlib, scikit-learn libraries
- Airflow 2.0 or higher

## Installation

1. Clone the repository: `git clone https://github.com/atharullah/pipeline_dashboard_design.git`
2. Install the required packages: `pip install -r requirements.txt`

## Section1: Data Pipelines

### Details

1. The pipeline expects CSV files to be dropped into the `/pipeline/data/input/` folder on an hourly basis.
2. The pipeline outputs successful applications into the `/pipeline/data/success/` folder and unsuccessful applications into the `/pipeline/data/failed/` folder.
3. Edit the Airflow DAG to set up the pipeline parameters as needed.

The datasets are formatted in the following manner:

1. Split name into first_name and last_name
2. Format birthday field into YYYYMMDD
3. Remove any rows which do not have a name field (treat this as unsuccessful applications)
4. Create a new field named above_18 based on the applicant's birthday
5. Membership IDs for successful applications should be the user's last name, followed by a SHA256 hash of the applicant's birthday, truncated to first 5 digits of hash (i.e <last_name>_<hash(YYYYMMDD)>)

The successful applications are consolidated and output into success folder, which will be picked up by downstream engineers. Unsuccessful applications are consolidated and dropped into failed folder.

### Running the pipeline

1. Start the Airflow webserver: `airflow webserver -p 8080`
2. Start the Airflow scheduler: `airflow scheduler`
3. Navigate to the Airflow UI in your browser: http://localhost:8080
4. Trigger the DAG manually or wait for the scheduler to pick up new files in the input folder.


## Section2: Databases

### Details
1. `Database` folder contains docker file, which will be created via task of DAG
2. `create_tables.sql`  contains schema design and copying to dcoker container which will run at start of container
3. `top_3_frequently_used.sql`, `top_10_member.sql` contains query as mentioned in requirements
4. `Entity_relationship.png` shows picture of database entity relationship.

## Section3: System Design

### Details
1. `system_design` folder contains both `drawio` diagram and `system_design.docx` contains system design details and explaination for both designs

## Section 4: Charts & APIs

### Details
1. `Dashboard` folder contains designs of covid data dashboard.

## Section 5: Machine Learning

### Details
1. `ML_Solution` folder contains solution of price prediction with data
