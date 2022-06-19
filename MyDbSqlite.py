import sqlite3

# Using connect method for establishing a connection
DATABASE_NAME = 'SQLite_ArnoldCat_Images.db'

class DB:
    def __init__(self) -> None:
        self.sqliteConnection = sqlite3.connect(DATABASE_NAME)
        self.cursor = self.sqliteConnection.cursor()
        print("Connected to SQLite")

        table = 'CREATE TABLE IF NOT EXISTS ArnoldCats (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, img BLOB NOT NULL);'
        self.cursor.execute(table)

    # Function for Convert Binary Data to Human Readable Format
    def convertToBinaryData(self, filename):
        
        # Convert binary format to images or files data
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData
    
    def insertBLOB(self, name, photo):
        try:
            # insert query
            sqlite_insert_blob_query = """ INSERT INTO ArnoldCats
                                    (id, name, img) VALUES (null, ?, ?)"""
            
            # Converting human readable file into binary data
            empPhoto = self.convertToBinaryData(photo)
            
            # Convert data into tuple format
            data_tuple = (name, empPhoto)
            
            # using cursor object executing our query
            self.cursor.execute(sqlite_insert_blob_query, data_tuple)
            self.sqliteConnection.commit()
            print("Image and file inserted successfully as a BLOB into a table")
            
        except sqlite3.Error as error:
            print("Failed to insert blob data into sqlite table", error)
    

    def writeTofile(self, data, filename):
        # Convert binary data to proper format and write it on Hard Disk
        with open(filename, 'wb') as file:
            file.write(data)
        print("Stored blob data into: ", filename, "\n")

    def readBlobData(self, empId):
        try:

            sql_fetch_blob_query = """SELECT * from ArnoldCats WHERE id = ?"""
            self.cursor.execute(sql_fetch_blob_query, (empId,))
            record = self.cursor.fetchall()
            for row in record:
                print("Id = ", row[0], "Name = ", row[1])
                name = row[1]
                photo = row[2]

                print("Storing ArnoldCats image on disk \n")
                photoPath = f"data/{name}.png"
                self.writeTofile(photo, photoPath)

        except sqlite3.Error as error:
            print("Failed to read blob data from sqlite table", error)

    def stop(self):
        self.cursor.close()
    



