#Impoting supporing modules
from sysinfo_collector import platform, psutil, ipaddress, datetime
#Importing functions used to retrieve system data
from sysinfo_collector import bytes_to_human, get_sysinfo, get_nicinfo, get_memoryinfo, get_diskinfo, get_cpuinfo

#Creatin a class representing current system statistics
class System:
    def __init__(self):
        self.sysinfo = get_sysinfo()
        self.cpuinfo, self.coredata = get_cpuinfo()
        self.memoryinfo = get_memoryinfo()
        self.diskinfo = get_diskinfo()
        self.nicinfo = get_nicinfo()
    
    def update_info(self):
        self.sysinfo = get_sysinfo()
        self.cpuinfo, self.coredata = get_cpuinfo()
        self.memoryinfo = get_memoryinfo()
        self.diskinfo = get_diskinfo()
        self.nicinfo = get_nicinfo()
    
    def print_info(self):
        print(self.sysinfo)
        print(self.cpuinfo)
        print(self.coredata)
        print(self.memoryinfo) 
        print(self.diskinfo)
        print(self.nicinfo)