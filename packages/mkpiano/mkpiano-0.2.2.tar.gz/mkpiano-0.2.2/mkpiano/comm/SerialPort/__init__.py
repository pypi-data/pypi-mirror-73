# -*- coding: utf-8 -*
import glob
import sys,os
import threading
from multiprocessing import Array, Manager, Process
from time import ctime, sleep
import serial.tools.list_ports
import serial
import mkpiano

def connect(port,baudrate=115200):
    """
    .. code-block:: python
        :linenos:

        from mkpiano import SerialPort
        from mkpiano import MegaPi

        uart = SerialPort.connect("COM3")
        board = MegaPi.connect(uart)

    """
    uart = SerialPort(port,baudrate)
    return uart

create = connect

class SerialPort():
    """
    """
    def __init__(self, port="/dev/ttyAMA0", baudrate=115200, timeout=1):
        self.exiting = False
        self._is_sending = True
        self._responses = []
        self._queue = []
        self._ser = None
        try:
            self._ser = serial.Serial(port,baudrate)
            self._ser.timeout = 0.01
            sleep(2)
            self._thread = threading.Thread(target=self._on_read,args=(self._callback,))
            self._thread.daemon = True
            self._thread.start()
            self._exit_thread = threading.Thread(target=self._on_exiting,args=())
            self._exit_thread.daemon = True
            self._exit_thread.start()
            mkpiano.add_port(self)
        except Exception as ex:
            print('$#&*@{"err_code":101,"err_msg":"串口被占用","device":"mkpiano","extra":"'+str(ex)+'“}@*&#$')

    def setup(self,callback):
        self._responses.append(callback)

    @property
    def type(self):
        return "uart"
        
    def _callback(self,received):
        for method in self._responses:
            method(received)

    def _on_read(self,callback):
        while True:
            if self.exiting:
                break
            if self._is_sending:
                self.__sending()
                    
            if self.is_open():
                # if self.in_waiting()>0:
                buf = self.read()
                if len(buf)==1:
                    callback(buf[0])
            # else:    
            #     sleep(0.001)

    def send(self,buffer):
        if self.is_open():
            self._queue.append(buffer)
        # sleep(0.002)

    def __sending(self):
        if len(self._queue)>0:
            if self.is_open():
                buf = self._queue[0]
                try:
                    self._ser.write(buf)
                except serial.serialutil.SerialException as e:
                    self.exiting = True
                    print("\033[1;33m连接失败，未检测到设备\033[0m")
                    print('$#&*@{"err_code":102,"err_msg":"发送数据失败，未检测到设备","device":"mkpiano","extra":{}}@*&#$')
                    return None
                self._queue.pop(0)

    def read(self):
        try:
            return self._ser.read()
        except serial.serialutil.SerialException as e:
            self.exiting = True
            print("\033[1;33m连接失败，未检测到设备\033[0m")
            print('$#&*@{"err_code":102,"err_msg":"读取数据失败，未检测到设备","device":"mkpiano","extra":{}}@*&#$')
            return []

    def enable_sending(self):
        self._is_sending = True

    def disable_sending(self):
        self._is_sending = False
        
    def _on_exiting(self):
        while True:
            if self.exiting:
                self.exit()
                break
    def is_open(self):
        if not self._ser is None:
            return self._ser.isOpen()
        return False

    def in_waiting(self):
        return self._ser.inWaiting()

    def close(self):
        self._ser.close()

    def exit(self):
        if not self._thread is None:
            self._is_sending = False
            self.exiting = True
            self._thread.join()
            self._thread = None
            self.close()
            os._exit(0)

    @staticmethod
    def list():
        """
        获取串口列表

        .. code-block:: python
            :linenos:

            from mkpiano import SerialPort
            print(SerialPort.list())

        :param: 无
        :return: 串口列表
        """
        return serial.tools.list_ports.comports()
