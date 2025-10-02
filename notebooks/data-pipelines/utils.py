# %%
import requests
import zipfile
import io
import json
import pprint
import time

#####################
# Define functions
#####################
#
# ####### check for validation errors #####
#
def check_for_fmr_validation_errors(report_data: dict) -> bool:
    """
    Extract value for Errors (boolean) in the given FMR validation report data.

    Parameters:
    report_data (dict): The FMR validation report data containing error information.

    Returns:
    errors: A boolean (True / False) indicating if any validation errors are found.
    """
    if not isinstance(report_data, dict):
        raise ValueError("report_data must be a dictionary.")   
        
    # Extract the value for Errors from the validation report.
    errors = report_data.get('Errors')
       
    return errors


#
# ####### print validation report #####
#
def  prettyprint_fmr_validation_report(report_data: dict):
    """
    Pretty Print the FMR validation report data to stdout.

    Parameters:
    report_data (dict): The FMR validation report data.

    Returns:
    """    
    # Prepare a textual summary report
    invalid_data = report_data.get('InvalidData', {})
    valid_data = report_data.get('ValidData', {})
    datasets = report_data.get('Datasets', [])

    # Calculate totals for the summary section
    total_valid_series = sum(dataset.get('Series', 0) for dataset in valid_data.get('Datasets', []))
    total_invalid_series = sum(dataset.get('Series', 0) for dataset in invalid_data.get('Datasets', []))

    summary = []
    
    # Add the summary section only if the report includes metrics
    # The presense of metrics is indicated by the total series > 0
    if total_valid_series + total_invalid_series > 0:
        summary.append("Summary:")
        summary.append(f"  {total_valid_series} valid series + {total_invalid_series} series with errors")
        summary.append("")

        summary.append("Invalid Data:")
        for dataset in invalid_data.get('Datasets', []):
            summary.append(f"  Structure: {dataset.get('Structure')}")
            summary.append(f"  Series: {dataset.get('Series')}")
            summary.append(f"  Observations: {dataset.get('Observations')}")
            summary.append(f"  Groups: {dataset.get('Groups')}")
        summary.append("")

        summary.append("Valid Data:")
        for dataset in valid_data.get('Datasets', []):
            summary.append(f"  Structure: {dataset.get('Structure')}")
            summary.append(f"  Series: {dataset.get('Series')}")
            summary.append(f"  Observations: {dataset.get('Observations')}")
            summary.append(f"  Groups: {dataset.get('Groups')}")
        summary.append("")

    summary.append("Datasets Summary:")
    for dataset in datasets:
        summary.append(f"  DSD: {dataset.get('DSD')}")
        summary.append(f"  Dataflow: {dataset.get('Dataflow')}")
        summary.append(f"  Series Count: {dataset.get('KeysCount')}")
        summary.append(f"  Observations Count: {dataset.get('ObsCount')}")
        summary.append(f"  Groups Count: {dataset.get('GroupsCount')}")
        reported_periods = dataset.get('ReportedPeriods', {})
        for period_key, period_value in reported_periods.items():
            summary.append(f"    Period {period_key}: {period_value.get('Name')} ({period_value.get('StartPeriod')} to {period_value.get('EndPeriod')})")
        validation_report = dataset.get('ValidationReport', [])
        for report in validation_report:
            summary.append("")
            summary.append(f"    Validation Rule: {report.get('Type')}")
            for error in report.get('Errors', []):
                summary.append(f"      Error Code: {error.get('ErrorCode')}")
                summary.append(f"      Message: {error.get('Message')}")
                summary.append(f"      Dataset: {error.get('Dataset')}")
                summary.append(f"      Position: {error.get('Position')}")
                summary.append(f"      Keys: {', '.join(error.get('Keys', []))}")
                if 'ComponentId' in error:
                    summary.append(f"      ComponentId: {error.get('ComponentId')}")
                if 'ReportedValue' in error:
                    summary.append(f"      Reported Value: {error.get('ReportedValue')}")
                    summary.append("")
    summary.append("")

    # Print the summary report to stdout
    print("\n".join(summary))
    
    return

def prettyprint_datafile (data_file_path):
    #
    # Read the contents of the datafile
    with open(data_file_path, 'r') as file:
        file_contents = file.read()
    pprint.pp(file_contents)
    return

def sync_validate(weservice_url, data_file_path, headers, auth):
    #
    # Read the contents of the datafile
    with open(data_file_path, 'r') as file:
        file_contents = file.read()

    # POST the data to valiate to the FMR's synchronous validation web service
    response = requests.post(weservice_url, data=file_contents, headers=headers, auth=auth, verify=False)

    # Check if request was successful
    if response.status_code == 200:
        # Check if the response is a ZIP file
        if response.headers.get('Content-Type') == 'application/zip':
            # Extract the ZIP file contents
            zip_file = zipfile.ZipFile(io.BytesIO(response.content))
            zip_file.extractall()  # Extract all files to the current working directory

            # Print a human readable summary of the JSON validation report
            with zip_file.open('report.json') as report_file:
                report_data = json.load(report_file)
            errors = check_for_fmr_validation_errors(report_data)
            if errors:
                print('Errors:', errors)
                print('Errors - Stop processing this file and action exception tasks ...')
                prettyprint_fmr_validation_report(report_data) # print the report for the sake of the demo
            else:
                print('File was processed successfully, continue doing useful things ...')
                prettyprint_fmr_validation_report(report_data) # print the report for the sake of the demo

        else:
            print('Error: The response is not a ZIP file')  
    
    else:
        print('NOT OK:', response.status_code)
        pprint.pp(response.text)
  
    return

def sync_transform (weservice_url, data_file_path, headers, auth):
    #
    # Read the contents of the datafile
    with open(data_file_path, 'r') as file:
        file_contents = file.read()

    # POST the data to valiate to the FMR's synchronous validation web service
    response = requests.post(weservice_url, data=file_contents, headers=headers, auth=auth, verify=False)

    Success = False
    # Check if request was successful
    if response.status_code == 200:
        # Check if the response is a ZIP file
        if response.headers.get('Content-Type') == 'application/zip':
            # Extract the ZIP file contents
            zip_file = zipfile.ZipFile(io.BytesIO(response.content))
            zip_file.extractall()  # Extract all files to the current working directory

            # Print a human readable summary of the JSON validation report
            with zip_file.open('metrics.json') as report_file:
                report_data = json.load(report_file)
            # You could check the report_data file for unmapped content and take whatever action is relevant for your workflows.
            print ("\nDump of the metrics.json file:")
            pprint.pp (report_data) # we will just print it so you can see what it looks like.
            errors = False # we do not have any error checks so lets assume all is ok.
            if errors:
                Success = False  # Validation errors in the data, take whatever action is relevant for your workflows.
                print('Errors:', errors)
                print('Errors - Stop processing this file and action exception tasks ...')
                prettyprint_fmr_validation_report(report_data) # print the report for the sake of the demo
            else:
                Success = True   # Rock and Roll Baby. Let's go.
        else:
            Success = False  # There response to the API call is not a ZIP file. Investigate.
    else:
        Success=False # There is an issue with the response code from the API call
        print('NOT OK:', response.status_code)
        print('Error Text', response.text)
    return Success

def async_load_the_source_data(api_entrypoint, data_file_path, input_type, urn_source):
    # The URL of the synchronous transformation web service is the <rest_entrypoint>/ws/public/data/validate
    # Reference : 
    weservice_url = f"{api_entrypoint}/ws/public/data/load"

    # Define the headers
    headers = {
        "Inc-Metrics" : "true", # include metrics in the validation report on the number of valid and invalid series and observations
        "Inc-Valid" : "true", # output the valid data as an SDMX dataset in a file called 'ValidData'
        "Inc-Invalid" : "true", # output the invalid data as an SDMX dataset in a file called 'InvalidData'
        "Zip" : "true", # return the output packaged as a ZIP file
        "Content-Type" : input_type, # the data for validation is in XML
        "Structure" : urn_source # Valid SDMX URN of the input (source) Dataflow or Data Structure Definition
    }

    print("\nSource data:")
    prettyprint_datafile(data_file_path)

    jobsuccess, jobid = async_load(weservice_url, data_file_path, headers)
    
    return jobsuccess, jobid


def async_load (weservice_url, data_file_path, headers, auth):
    # Call the FMR Validation web service and submit a file to be validated.
    #     
    # NOTE: response is a json file that looks like the following: 
    #       '{"Success":true,"uid":"06718286-d021-4c54-9a9f-b054c14d94ff"}'
    #
    payload = open(data_file_path)
    jobstatus = False
    jobid = ""

    try:
        response = requests.post(weservice_url, data=payload, headers=headers, timeout=10, auth=auth, verify=False)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)

        # If the request is successful (status code 200), process the JSON response
        data = response.json()
        #print("Success:", data)

        # Extracting values
        jobstatus = data.get("Success", False)  # Defaults to False if not found
        jobid = data.get("uid", "")  # Defaults to empty string if not found

    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} (Status Code: {response.status_code})")
    except requests.Timeout:
        print("Request timed out. Try again later.")
    except requests.ConnectionError:
        print("Connection error. Check your internet connection.")
    except requests.RequestException as req_err:
        print(f"An error occurred: {req_err}")
 
    return jobstatus, jobid

def async_check_load_status(weservice_url, jobid, CHECK_INTERVAL, auth):
    # The URL of the asynchronous load status web service
    # Reference : https://fmrwiki.sdmxcloud.org/Asynchronous_Data_Validation_and_Transformation_Web_Service
    params={'uid': jobid}
    errors = True

    """Checks the load status of the given jobid and waits until it is complete."""
    while True:
        try:
            response = requests.get(weservice_url, params=params, auth=auth, verify=False)
            response.raise_for_status()  # Raises an error for non-200 responses

            data = response.json()
            # pprint.pp(data)
            job_status = data.get("Status", "").lower()  #FIX - int() has no lower() # Assuming 'status' is in response
            
            if job_status == "complete":
                # print(f"Job {jobid} load and validation process has finished. There may / may not be errors.")
                if check_for_fmr_validation_errors (data) == True:
                    errors = True
                else:
                    errors = False
                break
            elif job_status in ["incorrectdsd", "invalidref", "missingdsd", "error"]:
                print(f"Job {jobid} has failed. Exiting.")
                errors = True
                return errors

            print(f"Job {jobid} is still in progress. Checking again in {CHECK_INTERVAL} seconds...")
            time.sleep(CHECK_INTERVAL)

        except requests.RequestException as e:
            print(f"Error checking job status: {e}. Retrying in {CHECK_INTERVAL} seconds...")
            time.sleep(CHECK_INTERVAL)
    return errors

def async_map_and_download (weservice_url, jobid, headers, auth):
    # ASYNCNRONOUS
    # ONCE "loadStatus" indicates "Status: Complete" and "Errors: false", the Validation has been completed and VALIDATION PASSED
    # 
    # IF  "loadStatus" indicates "Status: Complete" and "Errors: true", the Validation has been completed and VALIDATION FAILED
    # See FMR knowledge base for more response possibilities.
    #
    # Accept - subset of options:
    #   csv  : application/vnd.sdmx.data+csv
    #   json : application/vnd.sdmx.data+json
    #   xml  : application/vnd.sdmx.structurespecificdata+xml
    #
    params={'uid': jobid}

    r = requests.get(weservice_url, params=params, headers=headers, auth=auth, verify=False)
    #
    #pprint.pp(r.status_code)
    #pprint.pp(r.text)    

    return r.text