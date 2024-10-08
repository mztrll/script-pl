import socket

tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client_socket.connect(('localhost', 5252))

tcp_client_socket.sendall('Сообщение для сервера'.encode("utf-8"))
print('Cообщение отправлено на сервер')

response = tcp_client_socket.recv(1024)
print("Полученный ответ:", response.decode())

tcp_client_socket.close()