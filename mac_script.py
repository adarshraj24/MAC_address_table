### Script to capture known MAC addresses on all Cisco TORs
### me@viveksuthar.io

import paramiko
import getpass
import time
import csv


### Script Variables

csvPath = '/Users/ts-vivek.suthar/Desktop/ran_scripting/' # Path to script directory
csvFile = 'input.csv'                                     # Name of input csv file 
command = 'show mac address-table'                        # Command to run on TOR
torUser = 'root'                                          # Username for SSH to TOR


### Timestamp functionality for filename

timeStamp = time.strftime('%Y%m%d-%H%M%S')


### Capture Password for all TORs

pwd = getpass.getpass('TOR Password: ')


### Open Input CSV file with UHN and IPv6 for TORs

with open('{}{}'.format(csvPath,csvFile),'r') as torData:
    torData = csv.reader(torData,delimiter=',')
    torData = list(torData)
    torData.pop(0)


### Function to SSH Run command and capture output

def ssh_and_run(hostname,ipaddr):
    '''
    Use paramiko to ssh to IP address specifed in input csv file
    Redirect stdout to list called rawData
    Create a list of entry in rawData
    Remove 6 headder lines, insert title line with hostname
    Close SSH session
    '''
    
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ipaddr,username=torUser,password=pwd)
    stdin , stdout , stderr = ssh.exec_command(command)
    
    rawData = []
    for line in stdout:
        rawData.append(line)
        
    for entry in rawData:
        list(entry)
        
    cleanData = rawData[6:]
    cleanData.insert(
        0,' --------------------------- {} ---------------------------'.format(hostname)
    )
    cleanData.insert(1,'\n')
    cleanData.append('\n')
    
    ssh.close()
    
    return cleanData


### For every entry in input.csv, print the hostname and run function
### Append output of function to list called output

print('\n')
print('Getting MAC Data From: ')
output = []
for entry in torData:
    print('- ' + entry[:][0])
    x = ssh_and_run(entry[:][0],entry[:][-1])
    output.append(x)
    

### Open a file, and write entry 
    
with open('{}mac_table_{}.txt'.format(csvPath,timeStamp),'w') as outFile:
    for entry in output:
        for lines in entry:
            outFile.write('%s\n' % lines)
            
print('\n')
print('TOR MAC-Tables in following file: mac_table_{}.txt'.format(timeStamp))
print('\n')


