import shutil
import sqlite3
from datetime import datetime
from os import listdir
import os
import csv
from Application_Logging.logger import App_Logger


class DBOperations:

    def __init__(self):
        # self.training_good_file_path = 'F:/Data Science & AI/Internship Projects/CreditCardDefaulterPrediction/Training_ValidatedRawData/GoodDataFolder'
        # self.bad_data_folder = 'Training_ValidatedRawData/BadDataFolder'
        self.logger = App_Logger()
        self.logging_file_name = 'db_operations.txt'
        self.prediction_logging_file_name = 'Prediction_db_operations.txt'

        self.path = 'Prediction_Database/'

        self.badFilePath = "Training_ValidatedRawData/BadDataFolder"
        self.goodFilePath = "Training_ValidatedRawData/GoodDataFolder"
        # self.logger = App_Logger()

    def dataBaseConnection(self,DatabaseName):

        try:
            conn = sqlite3.connect(self.path+DatabaseName+'.db')
            self.logger.log(self.logging_file_name, "Opened %s database successfully" % DatabaseName)

        except ConnectionError:
            self.logger.log(self.logging_file_name, "Error while connecting to database: %s" %ConnectionError)
            raise ConnectionError
        return conn


    def createTableDb(self,DatabaseName,column_names):

        try:
            conn = self.dataBaseConnection(DatabaseName)
            conn.execute('DROP TABLE IF EXISTS Good_Raw_Data;')

            for key in column_names.keys():
                type = column_names[key]

                # we will remove the column of string datatype before loading as it is not needed for training
                #in try block we check if the table exists, if yes then add columns to the table
                # else in catch block we create the table
                try:
                    #cur = cur.execute("SELECT name FROM {dbName} WHERE type='table' AND name='Good_Raw_Data'".format(dbName=DatabaseName))
                    conn.execute('ALTER TABLE Good_Raw_Data ADD COLUMN "{column_name}" {dataType}'.format(column_name=key,dataType=type))
                except:
                    conn.execute('CREATE TABLE  Good_Raw_Data ({column_name} {dataType})'.format(column_name=key, dataType=type))

            conn.close()


            self.logger.log(self.logging_file_name, "Tables created successfully!!")
            self.logger.log(self.logging_file_name, "Closed %s database successfully" % DatabaseName)


        except Exception as e:

            self.logger.log(self.logging_file_name, "Error while creating table: %s " % e)
            conn.close()
            self.logger.log(self.logging_file_name, "Closed %s database successfully" % DatabaseName)
            raise e


    def insertIntoTableFromGoodData(self,Database):

        conn = self.dataBaseConnection(Database)
        goodFilePath= self.goodFilePath
        badFilePath = self.badFilePath

        onlyfiles = [f for f in listdir(goodFilePath)]


        for file in onlyfiles:
            try:
                # if os.path.isdir(goodFilePath):
                #     files = os.listdir(goodFilePath)
                #     for file in files:
                #         self.logger.log(self.logging_file_name, "Found a file in good data folder " + str(file))
                #         with open(goodFilePath + "/" + file, 'r') as data:
                #
                #             data_csv = csv.reader(data, delimiter=',')
                #             print(data_csv)
                #
                #             all_value = []
                #             self.logger.log(self.logging_file_name, "Starting insertion into the table")
                #             # for i in data_csv:
                #
                #         print('Finished')
                # else:
                #     self.logger.log(self.logging_file_name, "GoodDataFolder Doesn't Exist!!")

                with open(goodFilePath+'/'+file, "r") as f:
                    next(f)
                    reader = csv.reader(f, delimiter="\n")

                    self.logger.log(self.logging_file_name, "Insertion of data into the table started...please wait....")
                    for line in enumerate(reader):
                        for list_ in (line[1]):
                            try:
                                conn.execute('INSERT INTO Good_Raw_Data values ({values})'.format(values=(list_)))

                                conn.commit()
                            except Exception as e:
                                raise e
                    self.logger.log(self.logging_file_name, " %s: File loaded successfully!!" % file)

            except Exception as e:

                conn.rollback()
                self.logger.log(self.logging_file_name,"Error while creating table: %s " % e)
                shutil.move(goodFilePath+'/' + file, badFilePath)
                self.logger.log(self.logging_file_name, "File Moved Successfully %s" % file)

                conn.close()
                raise e

        conn.close()



    def selectingDatafromtableintocsv(self,Database):
        self.fileFromDb = 'Training_InputFileFromDB/'
        self.fileName = 'InputFile.csv'

        try:
            conn = self.dataBaseConnection(Database)
            sqlSelect = "SELECT *  FROM Good_Raw_Data"
            cursor = conn.cursor()

            cursor.execute(sqlSelect)

            results = cursor.fetchall()

            #Get the headers of the csv file
            headers = [i[0] for i in cursor.description]

            #Make the CSV ouput directory
            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)

            # Open CSV file for writing.
            csvFile = csv.writer(open(self.fileFromDb + self.fileName, 'w', newline=''),delimiter=',', lineterminator='\r\n',quoting=csv.QUOTE_ALL, escapechar='\\')

            # Add the headers and data to the CSV file.
            csvFile.writerow(headers)
            csvFile.writerows(results)

            self.logger.log(self.logging_file_name, "File exported successfully!!!")

        except Exception as e:
            self.logger.log(self.logging_file_name, "File exporting failed. Error : %s" %e)
            raise e





