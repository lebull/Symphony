import socket

UDP_IP = "192.168.255.255"
UDP_PORT = 4210
# MESSAGE = "Hello, World!"

# print "UDP target IP:", UDP_IP
# print "UDP target port:", UDP_PORT
# print "message:", MESSAGE
                    # Internet       # UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

def sendMessage(message):
    #print("send {} things".format(len(message)))
    sock.sendto(message, (UDP_IP, UDP_PORT))


