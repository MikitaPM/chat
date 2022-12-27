import socket, threading


nickname = input('Введите имя пользователя')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8081))


def receive():
    while True: #подтвеждение соединения
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICKNAME':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)

        except: # если не правильный ип или порт
            print('Ошибка')
            client.close()
            break


def write():# вывод сообщеия в чат
    while True:
        message = '{}:{}'.format(nickname, input(''))
        client.send(message.encode('utf-8'))


receive_thread = threading.Thread(target=receive) # Получение сообщения
receive_thread.start()
write_thread = threading.Thread(target=write) #отправка всех сообщения
write_thread.start()

