import pymysql.cursors
import json

def main():
    # Load json configuration file
    with open('config.json', 'r') as f:
        ARR = json.load(f)
    HOST = (ARR)['db-host']
    USER = (ARR)['db-username']
    PASSWORD = (ARR)['db-password']
    DBNAME = (ARR)['db-name']
    connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DBNAME, charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    # Output success. If connection failed. Program crashes.
    print("Success")
if __name__ == "__main__":
    main()