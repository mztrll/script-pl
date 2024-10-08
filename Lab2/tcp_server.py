import socket

# Создаем сокет
tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server_socket.bind(('localhost', 5252))

tcp_server_socket.listen()
print("Сервер находится в режиме ожидания подключения...")

client_socket, client_address = tcp_server_socket.accept()
print(f"Подключение установлено с {client_address}")
message = client_socket.recv(1024)
print(f"Полученное сообщение: {message.decode()}")

client_socket.sendall(message)
print('Cообщение отправлено обратно')

client_socket.close()
tcp_server_socket.close()