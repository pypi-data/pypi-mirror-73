from .boards import mbuild
import sys
import signal
import os,platform,ctypes,subprocess
from time import sleep
def driver_exist():
    system = platform.system()
    if system=="Darwin":
        kexts = "_".join(os.listdir("/Library/Extensions/"))
        return "usbserial.kext" in kexts
    elif system=="Windows":
        return "ch341ser.inf" in "_".join(os.listdir("C:\Windows\System32\DriverStore\FileRepository"))
    return True

def driver_install():
    if driver_exist():
        return True
    system = platform.system()
    try:
        if system=="Darwin":
            subprocess.call(["/usr/bin/open",os.path.dirname(__file__)+"/driver/ch34x_install.pkg"])
        elif system=="Windows":
            os.chdir(os.path.dirname(__file__)+"\\driver\\")
            if ctypes.windll.shell32.IsUserAnAdmin():
                subprocess.call([os.path.dirname(__file__)+"\\driver\\ch34x_install.exe","/sw","/se"])
            else:
                ctypes.windll.shell32.ShellExecuteW(None, "open", os.path.dirname(__file__)+"\\driver\\ch34x_install.exe", None, None, 1)
        while not driver_exist():
            sleep(1)
        return True
    except Exception as ex:
        pass
    return False

if driver_exist() == False:
    print("\033[1;32m设备驱动安装中...\033[0m")
    if driver_install() == False:
        print("\033[1;33m驱动安装失败\033[0m")
        print('$#&*@{"err_code":104,"err_msg":"驱动安装失败","device":"mkpiano","extra":{}}@*&#$')
        
_ports = []
_threads = []

def add_port(port):
    global _ports
    _ports.append(port)

def add_thread(thread):
    global _threads
    thread.daemon = True
    _threads.append(thread)

def quit():
    __exiting(0,0)
    
def __exiting(signal, frame):
    global _ports
    global _threads
    for port in _ports:
        port.exit()
    for thread in _threads:
        thread.exit()
    try:
        sys.exit(0)
    except Exception as e:
        print(e)

signal.signal(signal.SIGINT, __exiting)
piano = mbuild.piano
sleep(0.5)