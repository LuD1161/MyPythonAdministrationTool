import socket, sys
from thread import *

try:
    listening_ports = 8001
except KeyboardInterrupt:
    print("User interrupted")
    sys.exit()

max_conn = 5  # Max connection to hold
buffer_size = 8192  # Max socket buffer to hold
