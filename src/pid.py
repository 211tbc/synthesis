import platform
import subprocess

def get_processes():
    """Return a dictionary of process names where each value is a list
       of process ids belonging to the process"""

    processes = {}

    if platform.system() == "Linux":
        process_list = subprocess.Popen(['ps', '-A'], \
                        stdout=subprocess.PIPE).communicate()[0]

        # collapse whitespace in preparation to convert to a list
        while process_list.find("  ") >= 0:
               process_list = process_list.replace("  ", " ")

        process_list = process_list.split("\n")

        for i, ps in enumerate(process_list):
            process_list[i] = ps.strip()

        for p in process_list[1 : len(process_list) - 1]:
            info = p.split(" ")
            if processes.has_key(info[3]):
                processes[info[3]].append(info[0])
            else:
                processes[info[3]] = [info[0],]

    elif platform.system() == "Windows":
        #TODO:  Investigate the use of Windows' "tasklist" command ( http://technet.microsoft.com/en-us/library/bb491010.aspx )
        #       as a means to emulate what is done using the "ps" command on Linux
        pass

    return processes

def get_ids_of_process(process_name):
    """Given the process_name as a string, return a list of process ids
       belonging to a particular process"""
    processes = get_processes()
    pids = []
    if processes.has_key(process_name):
        pids = processes[process_name]

    return pids

def does_process_exist(process_name, process_ids):
    """Given the process_name as a string and a list of process_ids (normally
       generated with a call to get_ids_of_process), return True if all the
       process ids contained in process_ids are still active otherwise return
       False"""
    processes = get_processes()
    pids = []
    if processes.has_key(process_name):
        pids = processes[process_name]

    return set(process_ids).issubset(pids)


if __name__ == '__main__':
    pids = get_ids_of_process('paster')
    print pids

    print does_process_exist('paster', pids)
