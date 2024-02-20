from collections import defaultdict
import os
from pprint import pprint
import pyodbc
import boto3
from dotenv import load_dotenv

def get_db_connection_string():
    """Read the connection string from the env file and return it"""
    load_dotenv()

    # Access the environment variables
    server = os.getenv('SERVER')
    database = os.getenv('DATABASE')
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    driver = '{ODBC Driver 17 for SQL Server}'
    return f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"

def get_connections():
    connections = {}
    # Define the SQL query
    query = """SELECT  des.program_name
                , des.login_name
                , des.host_name
                , COUNT(des.session_id) [Connections]
            FROM    sys.dm_exec_sessions des
            INNER JOIN sys.dm_exec_connections DEC
                    ON des.session_id = DEC.session_id
            WHERE   des.is_user_process = 1
                    AND des.status != 'running'
                    AND des.program_name = '.Net SqlClient Data Provider'
            GROUP BY des.program_name
                , des.login_name
                , des.host_name
            HAVING  COUNT(des.session_id) > 2
            ORDER BY COUNT(des.session_id) DESC"""

    try:
        # Connect to the database
        connection = pyodbc.connect(get_db_connection_string())
        cursor = connection.cursor()

        cursor.execute(query)

        for row in cursor:
            connections[row[2]] = { 'connections': row[3], 'Name': ''}

    except pyodbc.Error as e:
        print(f"Error: {e}")

    finally:
        # Close the cursor and connection
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

    return connections

def get_ec2_instances():
    # Initialize Boto3 EC2 client
    ec2_client = boto3.client('ec2')

    # Define filters to retrieve instances for the PROD environment
    filters = [{'Name': 'tag:Environment', 'Values': ['prod']}]

    # Retrieve instances matching the filters
    response = ec2_client.describe_instances(Filters=filters)

    # Extract instance information
    instances = {}
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            host_name = ''
            name = ''
            if 'Tags' in instance:
                for tag in instance['Tags']:
                    if tag['Key'] == 'HostName':
                        host_name = tag['Value']
                    if tag['Key'] == 'Name':
                        name = tag['Value']
            instances[host_name] = name
            
    return instances
        
def main():
    connections = get_connections()
    ec2_instances = get_ec2_instances()
    
    for (key, value) in ec2_instances.items():
        if key in connections:
            connections[key]['Name'] = value  

    total_connections = sum([connection['connections'] for connection in connections.values()])
    print(f"Total connections: {total_connections}")

    grouped_connections = {}
    
    # Iterate through instances and accumulate connections by name
    for instance in connections.values():
        name = instance['Name']
        num_connections = instance['connections']
        if name in grouped_connections:
            grouped_connections[name] += num_connections
        else:
            grouped_connections[name] = num_connections
    
    sorted_connections = sorted(connections.items(), key=lambda x: x[1]['connections'], reverse=True)
    pprint(sorted_connections)
    
    pprint(grouped_connections)

if __name__ == "__main__":
    main()