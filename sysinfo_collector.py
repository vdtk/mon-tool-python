import json
import psutil
import platform
import ipaddress
import datetime

#Returns memory information in human-readable form
def bytes_to_human(nrofbytes, suffix = "B"):
    """Converts nrofbytes to human-readable form, returns a string"""

    factor = 1024
    #Iterates through units, each time dividing number of bytes by 1024, increasing unit value
    #When number of bytes, transformed converted to bigger unit, is less than 1024, returns {nrofbytes}{unit}{"B"}
    for unit in ["", "K", "M", "G", "T"]:
        if nrofbytes < 1024:
            return "%s%s%s" % (round(nrofbytes, 2), unit, suffix)
        nrofbytes = nrofbytes/factor

#GETTING HARDWARE AND SYSTEM INFO
def get_sysinfo():
    """Returns dictionary with values for key, based on system configuration.\n
       Following keys are present: system, node, release, version, machine, processor, local_time, boot_time."""

    #Storing object, containing all system and os information
    uname_result = platform.uname()
    #Storing system time and boot time
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).replace(microsecond=0)
    local_time = datetime.datetime.today().replace(microsecond=0)
    #Creating a dictionary, countainig all previously stored info
    sysinfo = {"system":uname_result.system, "node":uname_result.node, "release":uname_result.release,
               "version":uname_result.version, "machine":uname_result.machine, "processor":uname_result.processor,
               "local_time": str(local_time), "boot_time": str(boot_time)}
    return sysinfo

#GATHERING CPU INFORMATION
def get_cpuinfo():
    """Returns cpuinfo(dictionary), coredata(dictionary)\n
       Following keys are present in cpuinfo: physical_cpus, logical_cpus, max_frequency, min_frequency, current_frequency.\n
       For coredata, containing disk utilizaiton stats per core keys are: core [corenumber]"""

    #Storing utilization info per each logical core of the CPU
    cpu_utiliztion = psutil.cpu_percent(interval=1, percpu=True)
    #Creating a list with utilization data per core
    coredata = []
    #Creating a dictionary with CPU information
    cpuinfo = {"physical_cpus": psutil.cpu_count(logical=False), "logical_cpus": psutil.cpu_count(logical=True), "max_frequency": str(round(psutil.cpu_freq().max, 1)) + " Mhz",
               "min_frequency": str(round(psutil.cpu_freq().min, 1)) + " Mhz", "current_frequency": str(round(psutil.cpu_freq().current, 1)) + " Mhz"}
    #Filling the list with information per core
    for core in range(len(cpu_utiliztion)):
        coredata.append(["core "+str(core+1), str(cpu_utiliztion[core])+"%"])

    #Updating dictionary, containing all info with list we used previously to store info per core
    #For now, cpuinfo and coredata are separated
    #cpuinfo.update(dict(coredata))
    return cpuinfo, dict(coredata)

#GATHERING MEMORY INFORMATION
def get_memoryinfo():
    """Returns dictionary with values for key, based on system configuration.\n
       Following keys are present: total, available, used, percentage, swap_total, swap_free, swap_used, swap_percentage."""
    #Assigning an object, containing info about memory usage
    memory = psutil.virtual_memory()
    #Assigning an object with similar data for swap memory
    swap = psutil.swap_memory()
    #Creating a dictionary for all memeory data by referencing values of objects created previously
    meminfo = {"total": bytes_to_human(memory.total), "available": bytes_to_human(memory.available), "used": bytes_to_human(memory.used),
               "percentage": str(memory.percent)+"%", "swap_total": bytes_to_human(swap.total), "swap_free": bytes_to_human(swap.free),
               "swap_used": bytes_to_human(swap.used), "swap_percentage": str(swap.percent)+"%"}
    return meminfo

#GATHERING DISK INFORMATION
def get_diskinfo():
    """Returns a list, containing dictionary with stats per each partition.\n
       Keys for each dictionary are: partition, mountpoint, fstype, total_size, used, free."""
    #Storing information regarding disk partitions in a list of tuples
    partitions = psutil.disk_partitions()
    #Creating a list to store partition dictionaries
    all_partitions = []
    #Performing a proccess for each tuple in the list
    for partition in partitions:
        #Storing disk usage information of a partition by specifying it's mountpoint
        partition_usage = psutil.disk_usage(partition.mountpoint)
        #Appending a dictionary, containing partition information, disk usage informaiton for this partition
        all_partitions.append({"partition": partition.device, "mountpoint": partition.mountpoint, "fstype": partition.fstype,
                               "total_size": bytes_to_human(partition_usage.total), "used": bytes_to_human(partition_usage.used),
                               "free": bytes_to_human(partition_usage.free)})
    return all_partitions

#GATHERING NETWORK-INTERFACE INFO
def get_nicinfo():
    """Returns a list, containing dictionary with stats per each NIC.\n
       Keys for each dictionary are: interface_name, MAC, IPv4, IPv6."""
    #Saving a dictionary of key: interface name, value: interface addresses (a list of objects)
    if_addrs = psutil.net_if_addrs()
    #Creating a list to store dictionaries with data per interface
    all_interfaces = []
    #Iterating through dictionary
    for interface_name, interface_addresses in if_addrs.items():   
        #Per each interface key creating a dictionary to store interface information 
        interface_info = {}
        #Storing interface name info to the dictionary
        interface_info.update({"interface_name": interface_name})
        #Iterating through each address entry in value-list
        for data_entry in interface_addresses:
            #Storing address information depending on data format as MAC/IPv4/IPv6
            if len(data_entry.address) == 17:
                interface_info.update({"MAC": data_entry.address})
            else:
                new_address = ipaddress.ip_address(data_entry.address)
                if type(new_address) == ipaddress.IPv4Address:
                    interface_info.update({"IPv4": data_entry.address})
                if type(new_address) == ipaddress.IPv6Address:
                    interface_info.update({"IPv6": data_entry.address})
        all_interfaces.append(interface_info)
    return all_interfaces

# #Printing values to the command prompt
# print("="*20," SYSTEM INFO ", "="*20)
# print(json.dumps(get_sysinfo(), indent=4))

# print("="*20," CPU INFO ", "="*20)
# cpuinfo, coreinfo = get_cpuinfo()
# print(json.dumps(cpuinfo, indent=4))
# print(json.dumps(coreinfo, indent=4))

# print("="*20," MEMORY INFO ", "="*20)
# print(json.dumps(get_memoryinfo(), indent=4))

# #Printing info for partitions in json format
# print("="*20," PARTITION INFO ", "="*20)
# for partition in get_diskinfo():
#     print("\nPARTITION " + partition["partition"])
#     print(json.dumps(partition, indent=4))

# #Printing info for each interface in json format
# print("="*20," INTERFACES INFO ", "="*20)
# for interface in get_nicinfo():
#     print("\n" + interface["interface_name"])
#     print(json.dumps(interface, indent=4))
