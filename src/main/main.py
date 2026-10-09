import csv
import os
import sqlite3

# Resolve the resources folder relative to this file, so paths work
# no matter what directory the script is run from.
_RESOURCES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'resources')

# Connect to the SQLite in-memory database
conn = sqlite3.connect(':memory:')

# A cursor object to execute SQL commands
cursor = conn.cursor()


def main():

    # users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        userId INTEGER PRIMARY KEY,
                        firstName TEXT,
                        lastName TEXT
                      )'''
                   )

    # callLogs table (with FK to users table)
    cursor.execute('''CREATE TABLE IF NOT EXISTS callLogs (
        callId INTEGER PRIMARY KEY,
        phoneNumber TEXT,
        startTime INTEGER,
        endTime INTEGER,
        direction TEXT,
        userId INTEGER,
        FOREIGN KEY (userId) REFERENCES users(userId)
    )''')

    # You will implement these methods below. They just print TO-DO messages for now.
    load_and_clean_users(os.path.join(_RESOURCES_DIR, 'users.csv'))
    load_and_clean_call_logs(os.path.join(_RESOURCES_DIR, 'callLogs.csv'))
    write_user_analytics(os.path.join(_RESOURCES_DIR, 'userAnalytics.csv'))
    write_ordered_calls(os.path.join(_RESOURCES_DIR, 'orderedCalls.csv'))

    # Helper method that prints the contents of the users and callLogs tables. Uncomment to see data.
    select_from_users_and_call_logs()

    # Close the cursor and connection. main function ends here.
    cursor.close()
    conn.close()


# TODO: Implement the following 4 functions. The functions must pass the unit tests to complete the project.


# This function will load the users.csv file into the users table, discarding any records with incomplete data
def load_and_clean_users(file_path):
    with open(file_path, mode='r', newline='', encoding='utf-8') as user_records:
        # Create iterable object from users.csv file
        records = csv.reader(user_records)

        # Skip the header
        next(records)

        # Check each record if it contains exactly 2 fields and no empty values
        for row in records:
            if len(row) == 2 and ('' not in row):
                # Query to insert record into users table
                cursor.execute("INSERT INTO users (firstName, lastName) VALUES (?, ?)", row)


# This function will load the callLogs.csv file into the callLogs table, discarding any records with incomplete data
def load_and_clean_call_logs(file_path):
    with open(file_path, mode='r', newline='', encoding='utf-8') as call_logs:
        # Create iterable object from callLogs.csv file
        calls = csv.reader(call_logs)

        # Skip the header
        next(calls)

        # Check each record if it contains exactly 5 fields and no empty values
        for row in calls:
            if len(row) == 5 and ('' not in row):
                # Query to insert record into callLogs table
                cursor.execute("INSERT INTO callLogs (phoneNumber, startTime, endTime, direction, userId) VALUES (?, ?, ?, ?, ?)", row)

# This function will write analytics data to testUserAnalytics.csv - average call time, and number of calls per user.
# You must save records consisting of each userId, avgDuration, and numCalls
# example: 1,105.0,4 - where 1 is the userId, 105.0 is the avgDuration, and 4 is the numCalls.
def write_user_analytics(csv_file_path):
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as user_analytics:
        
        # Execute query to obtain userId, avgDuration, and numCalls
        cursor.execute(
            '''
            SELECT userId, AVG(endTime - startTime), COUNT(*)
            FROM callLogs
            GROUP BY userId
            '''
        )

        # Hold query output into rows to write into analytics file
        rows = cursor.fetchall()

        # Create iterable object to write into
        writer = csv.writer(user_analytics)

        # Set header
        writer.writerow(["userId", "avgDuration", "numCalls"])

        # For each row, write the record from the query's output
        writer.writerows(rows)



# This function will write the callLogs ordered by userId, then start time.
# Then, write the ordered callLogs to orderedCalls.csv
def write_ordered_calls(csv_file_path):
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as ordered_calls:
        # Write query to order userId and then start time
        cursor.execute(
            '''
            SELECT callId, phoneNumber, startTime, endTime, direction, userId
            FROM callLogs
            ORDER BY userId ASC, startTime ASC
            '''
        )

        # Store query results to write into file
        rows = cursor.fetchall()

        # Create iterable object to write into ordered file
        writer = csv.writer(ordered_calls)

        # Set header
        writer.writerow(["callId", "phoneNumber", "startTime", "endTime", "direction" , "userId"])

        # For each row, write the record from the query's output
        writer.writerows(rows)



# No need to touch the functions below!------------------------------------------

# This function is for debugs/validation - uncomment the function invocation in main() to see the data in the database.
def select_from_users_and_call_logs():

    print()
    print("PRINTING DATA FROM USERS")
    print("-------------------------")

    # Select and print users data
    cursor.execute('''SELECT * FROM users''')
    for row in cursor:
        print(row)

    # new line
    print()
    print("PRINTING DATA FROM CALLLOGS")
    print("-------------------------")

    # Select and print callLogs data
    cursor.execute('''SELECT * FROM callLogs''')
    for row in cursor:
        print(row)


def return_cursor():
    return cursor


if __name__ == '__main__':
    main()