import os
import pandas as pd
from Application_Logging.logger import App_Logger
from Training_RawDataValidation.raw_data_validation import RawDataValidation
from Training_DB_Operations.DB_operations import CassandraDBOperations
from Training_DB_Operations.db_operation import DBOperations



class TrainingFilesValidation:

    def __init__(self, path):
        self.file_name = 'TrainingFilesValidation.txt'
        self.log_writer = App_Logger()
        self.raw_data = RawDataValidation(path)
        # self.dBOperation = CassandraDBOperations()
        self.dBOperation = DBOperations()


    def train_validation(self):
        try:
            self.log_writer.log(self.file_name, "Entered into TrainingFilesValidation for training")
            # extracting values from prediction schema
            noofcolumns, column_names= self.raw_data.values_from_schema()

            # validating column length in the file
            self.log_writer.log(self.file_name, "Started Validating the columns length")
            self.raw_data.validate_column_length(noofcolumns)

            # validating if any column has all values missing
            self.log_writer.log(self.file_name, "Validating missing values in the whole column")
            self.raw_data.validateMissingValuesInWholeColumn()

            # replacing blanks in the csv file with "Null" values to insert in table
            # self.dataTransform.replaceMissingWithNull()

            # create database with given name, if present open the connection! Create table with columns given in schema
            self.log_writer.log(self.file_name, "Starting creating Table in sqlite")

            self.dBOperation.createTableDb('credit_card_training', column_names)

            # insert csv files in the table
            self.log_writer.log(self.file_name, "Inserting the data into table")
            self.dBOperation.insertIntoTableFromGoodData('credit_card_training')
            # self.dBOperation.insertIntoTableFromGoodData("credit_card1")

            # Delete the good data folder after loading files in table
            self.log_writer.log(self.file_name, "Deleting Existing Good Data Folder")
            self.raw_data.deleteExistingGoodDataRawFolder()

            # Move the bad files to archive folder
            self.log_writer.log(self.file_name, "Moving bad data folder to Archive")
            self.raw_data.moveBadFilesToArchiveBad()
            # export data in table to csvfile

            self.dBOperation.selectingDatafromtableintocsv('credit_card_training')

        except Exception as e:
            self.log_writer.log(self.file_name, "Something went wrong in TrainingFiles Validation.The exception is "+str(e))

