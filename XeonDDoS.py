from Core.Server import Server

ip = input('Enter IP >> ')
port = input('Enter Port >> ')
version = input('Enter Version (Example: 27) >> ')
thread_count = input('Enter Thread Count >> ')

port = int(port)
major = int(version)
thread_count = int(thread_count)

Server({'IP': ip, 'Port': port, 'Major': major,'ThreadCount': thread_count}).Start()