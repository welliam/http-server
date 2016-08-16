import socket
import sys
import utils


def client(message):
    if message == '':
        return ''
    infos = socket.getaddrinfo(*utils.address)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])

    client.connect(utils.address)
    client.sendall(message.encode('utf8') + utils.END)


    message = utils.recieve_message(client).decode('utf8')
    client.close()
    return message


if __name__ == '__main__':
    print(client(sys.argv[1]))