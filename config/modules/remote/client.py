import socket
import subprocess
import os
from colorama import *
init()

class SClient():
    def recvinstruction(self):
        client = socket.socket()

        in_out = input('[setup/client] in/out >> ')
        try:
            if in_out == 'in':
                localport = int(input('port >> '))
                client.connect(('localhost', localport))

            elif in_out == 'out':
                host = str(input('host >> '))
                port = int(input('port >> '))
                client.connect((host, port))

        except Exception as e:
            print("{}[Cat] Error: '{}'{}\n".format(Fore.RED,e,Style.RESET_ALL))

        while True:
            instruction = client.recv(3072)
            instruction = instruction.decode()
            instruction = instruction.split(" ")
            print(instruction) #test line
            try:
                execute = subprocess.run(instruction, stdout=subprocess.PIPE, shell=True)
                send_output = execute.stdout

            except Exception as e:
                error_msg = "Something went wrong, error: {}\n".format(e)
                error_msg = error_msg.encode()
                client.send(error_msg)

            else:
                try:
                    send_output = send_output.decode(encoding='ISO-8859-1')
                except UnicodeDecodeError:
                    send_output = send_output

                if send_output == '' or send_output == None:
                    emptyoutput = '.'
                    emptyoutput = emptyoutput.encode()
                    client.send(emptyoutput)

                else:
                    send_output = send_output.encode()
                    client.send(send_output)


            if instruction == "exit":
                print("{}>> client terminated <<\n{}".format(Style.BRIGHT+Fore.CYAN,Style.RESET_ALL))
                client.close()
                break

obj_client = SClient()
obj_client.recvinstruction()
