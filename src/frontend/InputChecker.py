from io import StringIO
import pandas as pd

class InputException(Exception):
    def __init__(self, msg):
        self.msg = msg

class InputChecker():
    columnTypes = {'Task_ID': True, 'Task_Name': True, 'Activity_ID': True, 'Activity_Name': True, 'Activity_Duration': False, 'Semaphore_ID': True, 'Semaphore_Name': True, 'Semaphore_Initial_Value': True, 'Predecessor_Semaphore_ID': True, 'Mutex_ID': True, 'Mutex_Name': True}
    
    # this method checks if the input is valid with various different other methods
    def checkInput(self, input, toApply=[]):
        df = None
        
        try:
            df = pd.read_csv(StringIO(input), sep=',')
            
            for func in toApply:
                func(df)
                
        except InputException as ie:
            return False, ie.msg
        
        except Exception:
            return False, "It seems like the data provided is not in CSV format."
            
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
        
    def checkEmptyCells(self, input):
        # check if there are empty cells
        for column in self.columnTypes.keys():
            if input[column].isnull().values.any():
                raise InputException("There are empty cells in the column '" + column + "'. Try using 'None' instead.")
    
    def checkForUniqueIDs(self, input):
        # check if the IDs are unique
        for column in ['Activity_ID', 'Semaphore_ID', 'Predecessor_Semaphore_ID']:
            if column == 'Predecessor_Semaphore_ID':
                predecessorSemaphores = self.__getAllPredecessorSemaphoreIDs(input)
                if len(predecessorSemaphores.unique()) != len(predecessorSemaphores):
                    for i, row in enumerate(predecessorSemaphores.value_counts()):
                        if row > 1:
                            raise InputException(f"Looks like semaphore {predecessorSemaphores[i]} is used multiple times as predecessor. Check for column 'Predecessor_Semaphore_ID'.")
            elif column == 'Semaphore_ID':
                semaphores = self.__getAllSemaphoreIDs(input)
                if len(semaphores.unique()) != len(semaphores):
                    for i, row in enumerate(semaphores.value_counts()):
                        if row > 1:
                            raise InputException(f"Looks like semaphore {semaphores[i]} is used multiple times as successor. Check for column 'Semaphore_ID'.")
            elif len(input[column].unique()) != len(input[column]):
                raise InputException("The IDs in the column '" + column + "' are not unique.")
    
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
    
    def checkColumnValues(self, input):
        # check if the column types are correct
        for column in self.columnTypes.keys():
            if self.columnTypes[column] == False:
                for row in input[column]:
                    if row == 'None':
                        raise InputException("The column '" + column + "' should be of type 'integer'.")
                    
                    if column == 'Activity_Duration':
                        if not isinstance(row, int):
                            raise InputException("The column '" + column + "' should be of type 'integer'.")
                        elif row < 0:
                            raise InputException("The column '" + column + "' should be positive.")
    
    def testPre(self, input):
        return self.__getAllPredecessorSemaphoreIDs(input)
    
    def test(self, input):
        return self.__getAllSemaphoreIDs(input)
    
    def __getAllSemaphoreIDs(self, input):
        if input['Semaphore_ID'].dtype == 'int64':
            return input['Semaphore_ID'].loc[input['Semaphore_ID'] != 'None'].astype(str)
        buf = input['Semaphore_ID'].str.split(';').apply(pd.Series).stack().reset_index(drop=True)
        return buf.loc[buf != 'None']
    
    def __getAllPredecessorSemaphoreIDs(self, input):
        if input['Predecessor_Semaphore_ID'].dtype == 'int64':
            return input['Predecessor_Semaphore_ID'].loc[input['Predecessor_Semaphore_ID'] != 'None'].astype(str)
        buf = input['Predecessor_Semaphore_ID'].str.split(';').apply(pd.Series).stack().reset_index(drop=True).apply(lambda x: x[1:-1] if x[0] == '[' and x[-1] == ']' else (x[1:] if x[0] == '[' else (x[:-1] if x[-1] == ']' else x)))
        return buf.loc[buf != 'None']