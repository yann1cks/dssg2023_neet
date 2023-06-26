import os
from dotenv import load_dotenv

# Load environment variables from the .env file

load_dotenv('..\..\.env')

# Read the input and output folder paths from the environment variables


def canonicalization(input_folder,output_folder,datasetype):
    # Iterate over all files in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.csv'):
            input_file = os.path.join(input_folder, file_name)
            file_name_without_pattern = file_name.rsplit('_', 1)[1]
            output_file = os.path.join(output_folder, f'{datasetype}_interim_{file_name_without_pattern}')
            # Escape backslashes in file paths
            input_file = input_file.replace('\\', '\\\\')
            output_file = output_file.replace('\\', '\\\\')
            print(f'Processing file: {input_file}')
            # Perform your analysis or processing on the input_file and save the results to the output_file
            os.system(f"python canonicalize.py  --inputs {input_file} --outputs {output_file} --dataset_type {datasetype}")
            # Replace the below print statements with your actual code
            print(f'Saving results to: {output_file}')
     
#Attendance Data        
input_folder_attendance_data = os.getenv('INPUT_ATTENDENCE_ORIGINAL_FOLDER')
output_folder_attendance_data = os.getenv('OUTPUT_ATTENDENCE_CANONICALIZED_FOLDER')
datasetype ='attendance'
canonicalization(input_folder_attendance_data,output_folder_attendance_data,datasetype)

#CCIS Data
input_folder_ccis_data = os.getenv('INPUT_CCIS_ORIGINAL_FOLDER')
output_folder_ccis_data = os.getenv('OUTPUT_CCIS_CANONICALIZED_FOLDER')
datasetype = 'ccis'
canonicalization(input_folder_ccis_data,output_folder_ccis_data,datasetype)

#Census Data
input_folder_census_data = os.getenv('INPUT_CENSUS_ORIGINAL_FOLDER')
output_folder_census_data = os.getenv('OUTPUT_CENSUS_CANONICALIZED_FOLDER')
datasetype = 'census'
canonicalization(input_folder_census_data,output_folder_census_data,datasetype)

#KS4 Data
input_folder_ks4_data = os.getenv('INPUT_KS4_ORIGINAL_FOLDER')
output_folder_ks4_data = os.getenv('OUTPUT_KS4_CANONICALIZED_FOLDER')
datasetype = 'ks4'
canonicalization(input_folder_ks4_data,output_folder_ks4_data,datasetype)

#characteristics Data
input_folder_characteristics_data = os.getenv('INPUT_CHARACTERISTICS_ORIGINAL_FOLDER')
output_folder_characteristics_data = os.getenv('OUTPUT_CHARACTERISTICS_CANONICALIZED_FOLDER')
datasetype = 'characteristics'
canonicalization(input_folder_characteristics_data,output_folder_characteristics_data,datasetype)

#School Info
input_folder_school_info_data = os.getenv('INPUT_SCHOOL_INFO_ORIGINAL_FOLDER')
output_folder_school_info_data = os.getenv('OUTPUT_SCHOOL_INFO_CANONICALIZED_FOLDER')
datasetype = 'school_info'
canonicalization(input_folder_school_info_data,output_folder_school_info_data,datasetype)


