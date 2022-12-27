import socket, threading # импорт библиотек


host = '127.0.0.1' # Локальный хост
port = 8081 # выбор незарезервированного порта

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Инициальизация сокета
server.bind((host, port))  # назначение хоста и порта к сокету
server.listen()

clients = []
nicknames = []


def broadcast(message):  # функция связи
    for client in clients:
        client.send(message)


def hendle(client):
    while True:
        try:  # получение сообщения от клиента
            message = client.recv(1024)
            broadcast(message)
        except:  # удаление клиентов
            index = client.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{}ушёл!'.format(nickname).encode('utf-8'))
            nicknames.remove(nickname)
            break


def receive():  # подлючение нескольких пользоателей
    while True:
        client, address = server.accept()
        print('Соединен с {}'.format(str(address)))
        client.send('NICKNAME'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        print("имя пользователя{}".format(nickname))
        broadcast("{}присоеднился".format(nickname).encode('utf-8'))
        client.send('Подключен к серверу'.encode('utf-8'))
        thread = threading.Thread(target=hendle, args=(client,))
        thread.start()


receive()
