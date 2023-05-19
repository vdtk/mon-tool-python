def create_tables(cur, db):
    try:
        # Creating the tables for system data
        # General system information
        cur.execute("""CREATE TABLE SYSINFO
                        (system text, node text, release text, version text, machine text, processor text, local_time text, boot_time text,
                        physical_cpus text, logical_cpus text, max_frequency text, min_frequency text, current_frequency text,
                        meminfo_total text, meminfo_available text, meminfo_used text, meminfo_percentage text, meminfo_swap_total text, meminfo_swap_free text, meminfo_swap_used text, meminfo_swap_percentage text)""")
        # Core utilization data
        cur.execute("""CREATE TABLE COREDATA
                       (node text, core text, data text)""")
        # Partition informaiton
        cur.execute("""CREATE TABLE PARTITIONS
                       (node text, partition text, mountpoint text, fstype text, total_size text, used text, free text)""")
        # Network interface data
        cur.execute("""CREATE TABLE NICS
                       (node text, interface_name text, MAC text, IPv4 text, IPv6 text)""")
        db.commit()
        print("Tables created")
    except:
        print("Tables created")
        pass

def add_sysinfo(client, cur, db):
    try:
        cur.execute("""DELETE FROM SYSINFO
                       WHERE node=?""", (client.sysinfo["node"], ))   
        cur.execute("""INSERT INTO SYSINFO VALUES
                   (?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?)""", 
                   (client.sysinfo["system"], client.sysinfo["node"], client.sysinfo["release"], client.sysinfo["version"], client.sysinfo["machine"], client.sysinfo["processor"], client.sysinfo["local_time"], client.sysinfo["boot_time"],
                    client.cpuinfo["physical_cpus"], client.cpuinfo["logical_cpus"], client.cpuinfo["max_frequency"], client.cpuinfo["min_frequency"], client.cpuinfo["current_frequency"],
                    client.memoryinfo["total"], client.memoryinfo["available"], client.memoryinfo["used"], client.memoryinfo["percentage"], client.memoryinfo["swap_total"], client.memoryinfo["swap_free"], client.memoryinfo["swap_used"], client.memoryinfo["swap_percentage"]))
        db.commit()
        print("SYSINFO ADDED")
    except Exception as e:
        print(e)
        print("SUBMITTING SYSINFO FAILED")
        db.rollback()

def add_coredata(client, cur, db):
    # Clearing all entries related to this client
    try:
        cur.execute("""DELETE FROM COREDATA
                       WHERE node = ?""", (client.sysinfo["node"], ))
        for key, value in client.coredata.items():
            cur.execute("""INSERT INTO COREDATA VALUES 
                           (?, ?, ?)""",
                           (client.sysinfo["node"], key, value))
        db.commit()
        print("CORADATA ADDED")
    except Exception as e:
        print(e)
        db.rollback()
        print("SUBMITTING COREDATA FAILED")

def add_partitions(client, cur, db):
    try:
        cur.execute("""DELETE FROM PARTITIONS
                       WHERE node = ?""", (client.sysinfo["node"], ))
        for partition in client.diskinfo:
            cur.execute("""INSERT INTO PARTITIONS VALUES 
                           (?, ?, ?, ?, ?, ?, ?)""",
                           (client.sysinfo["node"], partition["partition"], partition["mountpoint"], partition["fstype"], partition["total_size"], partition["used"], partition["free"]))
        db.commit()
        print("PARTITION INFO ADDED")
    except Exception as e:
        print(e)
        db.rollback()
        print("ADDING PARTITION INFO FAILED")

def add_nics(client, cur, db):
    try:
        cur.execute("""DELETE FROM NICS
                       WHERE node = ?""", (client.sysinfo["node"], ))
        for interface in client.nicinfo:
            MAC_adr, IPv4, IPv6 = None, None, None
            if "MAC" in interface:
                MAC_adr = interface["MAC"]
            if "IPv4" in interface:
                IPv4 = interface["IPv4"]
            if "IPv6" in interface:
                IPv6 = interface["IPv6"]

            cur.execute("""INSERT INTO NICS VALUES 
                           (?, ?, ?, ?, ?)""",
                           (client.sysinfo["node"], interface["interface_name"], MAC_adr, IPv4, IPv6))
        db.commit()
        print("NICS INFO ADDED")
    except Exception as e:
        print(e)
        db.rollback()
        print("ADDING NICS INFO FAILED")
