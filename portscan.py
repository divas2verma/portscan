import threading
import socket
from queue import Queue

target = input('Enter the target IP: ')
queue = Queue()
oports = []

print("Mode 1: Scan all 65535 TCP Ports")
print("Mode 2: Scan the commonly used ports")
print("Mode 3: Custom Port Scan Mode")
opt = int(input('Which option would you like to go ahead with: '))

def pscan(port):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect ((target, port))
		return True
	except:
		return False

def gports(opt):
    if opt == 1:
        for port in range(1, 65536):
            queue.put(port)
    elif opt == 2:
        ports = [80,443,21,22,110,995,143,993,25,26,587,3306,2082,2083,2086,2087,2095,2096,2077,2078]
        for port in ports:
            queue.put(port)
    elif opt == 3:
        ports = input("Enter your ports separated with *spaces*:")
        ports = ports.split()
        ports = list(map(int, ports))
        for port in ports:
            queue.put(port)

def worker():
	while not queue.empty():
		port = queue.get()
		if pscan(port):
			print("Port",port," is open!")
			oports.append(port)

def rscan(threads,opt):
	gports(opt)
	tlist = []
	for t in range (threads):
		thread = threading.Thread(target = worker)
		tlist.append(thread)

	for thread in tlist:
		thread.start()

	for thread in tlist:
		thread.join()

	print("Open ports are: ", oports)

i = int(input('Enter the number of threads: '))
rscan(i,opt)