import socket
 
udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 
udp_client_socket.sendto('Сообщение для сервера'.encode('utf-8'), ('localhost', 5252))
print('Cообщение отправлено на сервер')
 
response, client_address = udp_client_socket.recvfrom(1024)
print(f"Полученный ответ: {response.decode()}")

udp_client_socket.close()