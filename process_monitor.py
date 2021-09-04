#python script to let user to interact with the proceesses goin on.
#displays all the proceses

from datetime import datetime
from os import system
import  psutil
import  pandas as pd
import time
import os

#setting title of app
system("title " + "Prcoess Monitor")

def banner():
    print("""
                                                           ____             
 _ __  _ __ ___   ___ ___  ___ ___   _ __ ___   ___  _ __ (_) |_ ___  _ __ 
| '_ \| '__/ _ \ / __/ _ \/ __/ __| | '_ ` _ \ / _ \| '_ \| | __/ _ \| '__|
| |_) | | | (_) | (_|  __/\__ \__ \ | | | | | | (_) | | | | | || (_) | |   
| .__/|_|  \___/ \___\___||___/___/ |_| |_| |_|\___/|_| |_|_|\__\___/|_|   
|_|                                                                  Version 1.0      
                                                                            by naqviO7
""")


def get_processes_info():
    #list that will contain the processes
    processes=[]
    
    for process in psutil.process_iter():
        with process.oneshot():
            #getting process id
            pid=process.pid
            if pid==0:
                continue
            
            #getting name of process
            name=process.name()
            
            #getting time taken by process
            try:
                create_time=datetime.fromtimestamp(process.create_time())
            except OSError:
                create_time=datetime.fromtimestamp(psutil.boot_time())
            
            try:
                #getting cpu cores used by the process
                cores=len(process.cpu_affinity())
                
            except psutil.AccessDenied:
                cores=0 
            
            cpu_usage=process.cpu_percent()
            
            #getting process status
            status=process.status()
            
            try:
                # getting the process priority
                nice = int(process.nice())
            
            except psutil.AccessDenied:
                nice = 0
                
            try:
                # getting the memory usage in bytes
                memory_usage = process.memory_full_info().uss
            
            except psutil.AccessDenied:
                memory_usage = 0
            
            # total process read and written bytes
            io_counters = process.io_counters()
            read_bytes = io_counters.read_bytes
            write_bytes = io_counters.write_bytes
            
            # get the number of total threads spawned by this process
            n_threads = process.num_threads()
        
            # get the username of user spawned the process
            try:
                username = process.username()
            
            except psutil.AccessDenied:
                username = "N/A"
                
            processes.append({
                'pid': pid, 'name': name, 'create_time': create_time,
                'cores': cores, 'cpu_usage': cpu_usage, 'status': status, 'nice': nice,
                'memory_usage': memory_usage, 'read_bytes': read_bytes, 'write_bytes': write_bytes,
                'n_threads': n_threads, 'username': username,
            })

    return processes


def get_size(bytes):
    """
    Returns size of bytes in a nice format
    """
    
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024
        

def construct_dataframe(processes):
    # convert to pandas dataframe
    df = pd.DataFrame(processes)
    # set the process id as index of a process
    
    df.set_index('pid', inplace=True)
    
    # sort rows by the column passed as argument
    df.sort_values(sort_by, inplace=True, ascending=not descending)
    
    # pretty printing bytes
    df['memory_usage'] = df['memory_usage'].apply(get_size)
    df['write_bytes'] = df['write_bytes'].apply(get_size)
    df['read_bytes'] = df['read_bytes'].apply(get_size)
    
    # convert to proper date format
    df['create_time'] = df['create_time'].apply(
        datetime.strftime, args=("%Y-%m-%d %H:%M:%S",))
    
    # reorder and define used columns
    df = df[columns.split(",")]
    
    return df


if __name__ == "__main__":
    #clear screen    
    os.system("cls")
    time.sleep(2)
    
    banner()
    
    time.sleep(2)

    import argparse
    
    parser = argparse.ArgumentParser(description="Process Viewer & Monitor")
    
    parser.add_argument("-c", "--columns", help="""Columns to show,
                                                available are name,create_time,cores,cpu_usage,status,nice,memory_usage,read_bytes,write_bytes,n_threads,username.
                                                Default is name,cpu_usage,memory_usage,read_bytes,write_bytes,status,create_time,nice,n_threads,cores.""",
                        default="name,cpu_usage,memory_usage,read_bytes,write_bytes,status,create_time,nice,n_threads,cores")
    
    parser.add_argument("-s", "--sort-by", dest="sort_by",
                        help="Column to sort by, default is memory_usage .", default="memory_usage")
    
    parser.add_argument("--descending", action="store_true",
                        help="Whether to sort in descending order.")
    
    parser.add_argument(
        "-n", help="Number of processes to show, will show all if 0 is specified, default is 25 .", default=25)
    
    parser.add_argument("-u", "--live-update", action="store_true",
                        help="Whether to keep the program on and updating process information each second")

    # parse arguments
    args = parser.parse_args()
    columns = args.columns
    sort_by = args.sort_by
    descending = args.descending
    n = int(args.n)
    live_update = args.live_update
    
    # print the processes for the first time
    processes = get_processes_info()
    
    df = construct_dataframe(processes)
    
    if n == 0:
        print(df.to_string())
    elif n > 0:
        print(df.head(n).to_string())
    
    # print continuously
    while live_update:
        # get all process info
        processes = get_processes_info()
        df = construct_dataframe(processes)
        # clear the screen depending on your OS
        os.system("cls") if "nt" in os.name else os.system("clear")
        if n == 0:
            print(df.to_string())
        elif n > 0:
            print(df.head(n).to_string())
        time.sleep(0.7)


#END OF CODE
