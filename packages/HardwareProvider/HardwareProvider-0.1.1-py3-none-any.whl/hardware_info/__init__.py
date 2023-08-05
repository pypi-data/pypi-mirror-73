"""
This is a module used to get hardware info
"""


import psutil
import cpuinfo
import math
import platform
from datetime import datetime


class CPU:
    
    info = cpuinfo.get_cpu_info()
    
    @staticmethod
    def cpu_cores(hyperthreading = False):
        return psutil.cpu_count(logical = hyperthreading)
    
    
    @staticmethod
    def architecture():
        return CPU.info['arch']
    
    
    @staticmethod
    def name():
        return CPU.info['brand_raw']
    
    @staticmethod
    def percent():
        return psutil.cpu_percent(0.2) 
    
    
class Ram:
    
    mem = psutil.virtual_memory()
    
    @staticmethod
    def total_mem(acc):
        return round(Ram.mem.total/1000000000, acc)
    
    @staticmethod
    def used_mem(acc):
        return round(Ram.mem.used/1000000000, acc)
    
    @staticmethod
    def free_mem(acc):
        return round(Ram.mem.available/1000000000, acc)
    
  
class Disk:
    
    @staticmethod
    def list_disks(every = False):
        return [{'device': i[0], 'mountpoint': i[1], 'fstype': i[2], 'opts': i[3]} for each in psutil.disk_partitions(all=every) if (i:=list(each))]

    @staticmethod
    def get_size(bts, suffix="B"):
        """
        Scale bytes to its proper format
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        """
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bts < factor:
                return f"{bts:.2f}{unit}{suffix}"
            bts /= factor
        
        
    @staticmethod
    def total_r_and_w():
        disk_io = psutil.disk_io_counters()
        return {'read': Disk.get_size(disk_io.read_bytes), 'write': Disk.get_size(disk_io.write_bytes)}
    
    @staticmethod
    def space(every=False):
        partitions = psutil.disk_partitions(all=every)
        to_return = {}
        for partition in partitions:
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                # this can be catched due to the disk that
                # isn't ready
                continue
            to_return[(partition.device, partition.mountpoint, partition.fstype)] = {
                'total': Disk.get_size(partition_usage.total), 
                'used': Disk.get_size(partition_usage.used),
                'free': Disk.get_size(partition_usage.free),
                'usage_percentage': partition_usage.percent

            }
        return to_return


class Network:
    
    @staticmethod
    def get_ip():
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = None
        finally:
            s.close()
        return IP
  
  
  
class OS:
    
    @staticmethod
    def name():
        return [platform.system(), platform.release()]
    
    @staticmethod
    def hardware(more = False):
        if platform.system() == 'Windows':
            import wmi

            computer = wmi.WMI()
            
            if more:
                cpus = [proc for proc in computer.Win32_Processor()]
                gpus = [gpu for gpu in computer.Win32_VideoController()]
                
            else:
                cpus = [proc.name for proc in computer.Win32_Processor()]
                gpus = [gpu.name for gpu in computer.Win32_VideoController()]
                
            return {'cpus': cpus, 'gpus': gpus}
    
        else:
            return None
        
    
    @staticmethod
    def users():
        return psutil.users()
    
    @staticmethod
    def fans_rpm():
        if platform.system == 'Linux':
            return psutil.sensors_fans()
        return None
    
    
    @staticmethod
    def temp(fahrenheit=False):
        if platform.system == 'Linux':
            return psutil.sensors_temperatures(fahrenheit=fahrenheit)
        return None
    
    
    @staticmethod
    def battery_info():
        info = (list(psutil.sensors_battery()))
        return {'Percentage': info[0], 'SecondLeft': info[1], 'MinutesLeft': round(info[1]/60), 'HoursLeft': round(info[1]/1440, 2), 'PluggedIn': info[2]}
