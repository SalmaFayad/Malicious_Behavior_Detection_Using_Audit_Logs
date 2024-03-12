import os
import pandas as pd
from lxml import etree
import codecs

def wrap_with_events(xml_file_path):
    try:
        encodings = ['utf-8', 'utf-16', 'latin-1']

        # Try different encodings until successful
        for encoding in encodings:
            try:
                # Read the entire XML file as a string
                with open(xml_file_path, 'r', encoding=encoding) as file:
                    xml_content = file.read()

                # Wrap the XML content with <Events> tags
                wrapped_xml = f'<Events>\n{xml_content}\n</Events>'

                # Save the modified XML back to the original file
                with open(xml_file_path, 'w', encoding='utf-8') as modified_file:
                    modified_file.write(wrapped_xml)

                print(f"XML file has been modified and saved to {xml_file_path}")
                return

            except UnicodeDecodeError:
                continue

        print("Error: Unable to determine the correct encoding.")

    except Exception as e:
        print(f"Error: {e}")

def read_xml(file_path):
    parser = etree.XMLParser(recover=True)

    # Open the file using codecs to handle BOM
    with codecs.open(file_path, encoding="utf-8-sig") as file:
        data = file.read()

    raw = etree.fromstring(data, parser=parser)
    return raw

def events_to_df(eventlist, selected_features):
    df_list = []
    tag = '{http://schemas.microsoft.com/win/2004/08/events/event}'
    for idx, event in enumerate(eventlist):
        edict = {feature: None for feature in selected_features}
        for element in event.iterdescendants():
            if any(x in element.tag for x in ['TimeCreated', 'Execution', 'Security']):
                for item in element.items():
                    edict[item[0]] = item[1]
            elif any(x in element.tag for x in ['Provider', 'System', 'Correlation']):
                pass
            elif 'Data' in element.tag:
                for item in element.items():
                    edict[item[1]] = element.text
            else:
                edict[element.tag.replace(tag, '')] = element.text

        edict['raw'] = etree.tostring(event, pretty_print=True).decode()

        edf = pd.DataFrame(edict, index=[idx])
        df_list.append(edf)

    return pd.concat(df_list, sort=True)

def apply_fixed_length(df, column_lengths, selected_features):
    for column in selected_features:
        if column in df.columns:
            length = column_lengths.get(column, 0)
            df[column] = df[column].astype(str).str.ljust(length, '0')
    return df

def combine_columns(row, selected_features):
    return ''.join([str(row[column]) for column in selected_features])

def process_xml_folder(folder_path, column_lengths, selected_features):
    df_list = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".xml"):
            xml_file_path = os.path.join(folder_path, filename)
            xml_data = read_xml(xml_file_path)
            events = [element for element in xml_data.iter('{http://schemas.microsoft.com/win/2004/08/events/event}Event')]
            log_df = events_to_df(events, selected_features)

            df_list.append(log_df)

    # Concatenate all dataframes after processing XML files
    result_df = pd.concat(df_list, ignore_index=True)

    # Select only specified features
    result_df = result_df[selected_features]

    # Replace null values with 0
    result_df.fillna(0, inplace=True)

    # Apply fixed length to selected columns
    result_df = apply_fixed_length(result_df, column_lengths, selected_features)

    # Combine all columns into a single column
    result_df['combined'] = result_df.apply(lambda row: combine_columns(row, selected_features), axis=1)

    # Drop the original columns
    result_df.drop(columns=selected_features, inplace=True)

    # Transpose the DataFrame
    result_df_transposed = result_df.transpose()

    # Save the transposed DataFrame to a CSV file without header
    result_df_transposed.to_csv('data.csv', index=False, header=False)

# Define the column lengths
# Define the column lengths
column_lengths = {
    "CommandLine": 350,
    "Company": 36,
    "CurrentDirectory": 94,
    "DestinationIsIpv6": 5,
    "DestinationPort": 4,
    "DestinationPortName": 13,
    "Details": 269,
    "EventID": 2,
    "EventType": 12,
    "FileVersion": 59,
    "Initiated": 4,
    "IntegrityLevel": 6,
    "Level": 12,
    "Message": 500,
    "ParentCommandLine": 500,
    "ParentUser": 29,
    "Product": 39,
    "Protocol": 3,
    "QueryName": 254,
    "QueryResults": 400,
    "QueryStatus": 5,
    "RuleName": 35,
    "SourceImage": 58,
    "SourceIsIpv6": 5,
    "SourcePort": 5,
    "SourcePortName": 1,
    "StartFunction": 12,
    "StartModule": 35,
    "TargetFilename": 204,
    "TargetImage": 48,
    "TargetUser": 20,
    "Task": 55,
}

# Define the selected features
selected_features = [
    "CommandLine", "Company", "CurrentDirectory", "DestinationIsIpv6", "DestinationPort",
    "DestinationPortName", "Details", "EventID", "EventType", "FileVersion", "Initiated",
    "IntegrityLevel", "Level", "Message", "ParentCommandLine", "ParentUser", "Product",
    "Protocol", "QueryName", "QueryResults", "QueryStatus", "RuleName", "SourceImage",
    "SourceIsIpv6", "SourcePort", "SourcePortName", "StartFunction", "StartModule",
    "TargetFilename", "TargetImage", "TargetUser", "Task"
]

# Provide the folder path containing XML files
xml_folder_path = "xml"

# Call the function to modify XML files in place
for filename in os.listdir(xml_folder_path):
    if filename.endswith(".xml"):
        xml_file_path = os.path.join(xml_folder_path, filename)
        wrap_with_events(xml_file_path)

# Call the function to process the XML folder and save the result to a CSV file
process_xml_folder(xml_folder_path, column_lengths, selected_features)
