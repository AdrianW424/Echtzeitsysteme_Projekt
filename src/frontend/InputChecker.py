from io import StringIO
import pandas as pd

class InputException(Exception):
    def __init__(self, msg):
        self.msg = msg

class InputChecker():
    columnTypes = {'Task_ID': 'str', 'Task_Name': 'str', 'Activity_ID': 'str', 'Activity_Name': 'str', 'Activity_Duration': 'int', 'Semaphore_ID': 'str|list(str)', 'Semaphore_Name': 'str|list(str)', 'Semaphore_Initial_Value': 'int|list(int)', 'Predecessor_Semaphore_ID': 'str|list(str)', 'Mutex_ID': 'str|list(str)', 'Mutex_Name': 'str|list(str)'}
    
    # this method checks if the input is valid with various different other methods
    def checkInput(self, input, toApply=[]):
        df = None
        
        try:
            df = pd.read_csv(StringIO(input), sep=',')
            
            # for func in toApply:
            #     func(df)
                
        except InputException as ie:
            return False, ie.msg
        
        # except Exception:
        #     return False, "It seems like the data provided is not in CSV format."
            
        return True, df
    
    def checkColumns(self, input):
        # check if the columns are correct

        input_columns = input.columns
        for column in self.columnTypes.keys():
            if column not in input_columns:
                raise InputException("The column '" + column + "' is missing.")
            else:
                input_columns = input_columns.drop(column)
        
        if not input_columns.empty:
            raise InputException("The column '" + input_columns[0] + "' is not needed.")
    
    def checkColumnTypes(self, input):
    
        for columnType in self.columnTypes:
            if self.columnTypes[columnType] == 'int':
                if not input[columnType].dtype == 'int64':
                    if not (columnType == 'Semaphore_Initial_Value' and input[columnType][0] == 'None'):
                        raise InputException("The column '" + columnType + "' is not of the correct type. It should be of type 'int'.")
            elif self.columnTypes[columnType] == 'int|list(int)':
                if input[columnType].dtype != 'int64':
                    for row in input[columnType].str.split(';'):
                        for value in row:
                            try:
                                if columnType == 'Semaphore_Initial_Value' and value == 'None':
                                    continue
                                int(value)
                            except:
                                raise InputException("The column '" + columnType + "' is not of the correct type. It should be of type 'int' or 'list(int)'.")
    
    def checkEmptyCells(self, input):
        # check if there are empty cells
        for column in self.columnTypes.keys():
            if input[column].isnull().values.any():
                raise InputException("There are empty cells in the column '" + column + "'. Try using 'None' instead.")
    
    def checkSemaphores(self, input):
        predecessorSemaphores = self.__getAllPredecessorSemaphoreIDs(input)
        outgoingSemaphores = self.__getAllSemaphoreIDs(input)
        
        # check if the predecessor semaphores are in the list of semaphores
        # also have to consider OR-groups
        
        for semaphore in predecessorSemaphores:
            if semaphore not in outgoingSemaphores.values:
                raise InputException("The semaphore '" + semaphore + "' has no beginning.")
                    
        # check if the semaphores are in the list of predecessor semaphores
        
        for semaphore in outgoingSemaphores:
            if semaphore not in predecessorSemaphores.values:
                raise InputException("The semaphore '" + semaphore + "' has nowhere to go.")
        
    def checkForUniqueIDs(self, input):
        # check if the IDs are unique
        for column in ['Activity_ID', 'Semaphore_ID', 'Predecessor_Semaphore_ID']:
            if column == 'Predecessor_Semaphore_ID':
                predecessorSemaphores = self.__getAllPredecessorSemaphoreIDs(input)
                if len(predecessorSemaphores.unique()) != len(predecessorSemaphores):
                    raise InputException("Looks like some semaphores are used multiple times as predecessors. Check for column 'Predecessor_Semaphore_ID'.")
            elif column == 'Semaphore_ID':
                semaphores = self.__getAllSemaphoreIDs(input)
                if len(semaphores.unique()) != len(semaphores):
                    raise InputException("Looks like some semaphores are used multiple times as successors. Check for column 'Semaphore_ID'.")
            elif len(input[column].unique()) != len(input[column]):
                raise InputException("The IDs in the column '" + column + "' are not unique.")
            
    def test(self, input):
        return self.__getAllPredecessorSemaphoreIDs(input)
    
    def __getAllSemaphoreIDs(self, input):
        return input['Semaphore_ID'].str.split(';').apply(pd.Series).stack().reset_index(drop=True)
    
    def __getAllPredecessorSemaphoreIDs(self, input):
        return input['Predecessor_Semaphore_ID'].str.split(';').apply(pd.Series).stack().reset_index(drop=True).apply(lambda x: x[1:-1] if x[0] == '[' and x[-1] == ']' else (x[1:] if x[0] == '[' else (x[:-1] if x[-1] == ']' else x)))