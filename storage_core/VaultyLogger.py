import datetime
import time

class VaultyLogger:
    def __init__(self,file):
        self.file = file

    def getTimestamp(self):
        current_time = datetime.datetime.now()
        day_no = current_time.day
        month = current_time.strftime("%B")
        year = current_time.year
        time = current_time.strftime("%H:%M:%S")
        timestamp = "{0};{1} {2} {3}".format(time,day_no,month,year)
        return timestamp

    def log(self,log_type,description):
        # Appending at the top of file is creating aux file or loading complete file
        # { vlog# [log-no];[time-stamp];[log-type];[description] }
        timestamp = self.getTimestamp()
        f = open(self.file,'a+')
        logString = "\nVLOG;{0};{1};{2}".format(timestamp,log_type,description)
        f.write(logString)

# Helper Log Search Function
def binary_search_logs(log_file,target_date):
    target_datetime = datetime.datetime.strptime(target_date,'%d %B %Y')
    with open(log_file,'r') as file:
        data = file.readlines()
    return _internal_binary_search_logs(data,target_datetime)

def _internal_binary_search_logs(data, target_datetime):
    logs = [] 
    low = 0
    high = len(data) - 1  # Adjusted the high value to prevent out of range access

    while low <= high:
        mid = (low + high) // 2
        log_data = data[mid].split(';')[2]
        x_datetime = datetime.datetime.strptime(log_data,'%d %B %Y')

        if x_datetime == target_datetime:
            logs.append(data[mid])

            i = mid - 1
            while i >= 0 and datetime.datetime.strptime(data[i].split(';')[2],'%d %B %Y') == target_datetime:
                logs.append(data[i])
                i -= 1
            
            j = mid + 1
            while j <= len(data) - 1 and datetime.datetime.strptime(data[j].split(';')[2],'%d %B %Y') == target_datetime:
                logs.append(data[j])
                j += 1

            return logs
        elif x_datetime > target_datetime:
            high = mid - 1
        else:
            low = mid + 1

    return logs

# Example usage
#log_file = 'vlog.txt'
#target_date = '13th July 2024'

#result = binary_search_logs(log_file, target_date)
#for log in result:
#    print(log)  # Print the logs for the specified date

#v = VaultyLogger("vlog.txt")
#for i in range(3):
#    v.log("CLIENT_AUTATION","This is been add")


'''
Log the following data:
- Timestamp data
- Log Number
- Description ("")
- Log Type: CLIENT_AUTHENTICATION, DATABASE_READ, DATABASE_WRITE
            VAULT_CREATION, VAULT_DELETION, VAULT_DECRYPTION,
            VAULT_MODIFICATION, FILE_TRANSFER, STARTUP
            
Example:
{ vlog# [log-no] [time-stamp] [log-type] [description] }
'''