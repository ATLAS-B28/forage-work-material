import csv
import sqlite3

def create_tab(cursor):
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS shipping_data_0 (
            origin_warehouse TEXT,
            destination_store TEXT,
            product TEXT,
            on_time TEXT,
            product_quantity INTEGER,
            driver_identifier TEXT
        )
     """)
    
    cursor.execute("""
         CREATE TABLE IF NOT EXISTS shipping_data_1 (
            shipment_identifier TEXT,
            product TEXT,
            on_time TEXT,
            origin_warehouse TEXT,
            destination_store TEXT
        )
      """)
    
#insert from shipping data 0 csv
def insert_shipping_0(cursor):
    with open('data\shipping_data_0.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            origin_warehouse, destination_store, product, on_time, product_quantity, driver_identifier = row
            cursor.execute("INSERT INTO shipping_data_0 (origin_warehouse, destination_store, product, on_time, product_quantity, driver_identifier) VALUES (?, ?, ?, ?, ?, ?)", 
                           (origin_warehouse, destination_store, product, on_time, product_quantity, driver_identifier))
            
#FROM 2
def insert_shipping_2(cursor):
    with open('data\shipping_data_2.csv','r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        #append data from here to a list
        shipping_data_2_rows_as_list = [row for row in csv_reader]#save the 3 rows from here in a list

    #now go to 1st csv
    with open('data\shipping_data_1.csv','r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:#assign the 3 rows from the csv-1
            shipment_identifier, product, on_time = row
            matching_shipment_row = [r for r in shipping_data_2_rows_as_list if r[0] == shipment_identifier]#match the 1st rows of the csv-1 and csv-2
            if matching_shipment_row:#if list is not empty, assign the 3 rows from the csv-2 (1st is already there, the last 3 ones)
                origin_warehouse, destination_store, driver_identifier = matching_shipment_row[0][1], matching_shipment_row[0][2], matching_shipment_row[0][3]
                cursor.execute("INSERT INTO shipping_data_1 (shipment_identifier, product, on_time, origin_warehouse, destination_store) VALUES (?, ?, ?, ?, ?)", 
                               (shipment_identifier, product, on_time, origin_warehouse, destination_store))#and insert them in the 1st csv related database
                
if __name__ == "__main__":
    conn = sqlite3.connect('shipment_database.db')
    cursor = conn.cursor()

    create_tab(cursor)

    insert_shipping_0(cursor)
    insert_shipping_2(cursor) 

    conn.commit()
    conn.close()             