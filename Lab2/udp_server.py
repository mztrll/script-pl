import socket

udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server_socket.bind(('localhost', 5252))

print("Ожидание получения данных...")

message, client_address = udp_server_socket.recvfrom(1024)
print(f"Сообщение получено от {client_address}")
print(f"Полученное сообщение: {message.decode()}")

udp_server_socket.sendto(message, client_address)
print('Cообщение отправлено обратно')

udp_server_socket.close()