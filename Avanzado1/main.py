import sys
import csv
import os
# clients = [
#         {
#                 'name' : 'Pablo',
#                 'company' : 'Google',
#                 'email' : 'pablo@gmail.com',
#                 'position' : 'Software engineer'
#         },
#         {
#                 'name' : 'Ricardo',
#                 'company' : 'facebook',
#                 'email' : 'ricardo@gmail.com',
#                 'position' : 'Data Engineer'
#         }
# ]
CLIENT_TABLE = "clients.csv"
CLIENT_SCHEMA = ['name','company','email','position']
clients = []

def _inicializa_clients_from_storage():
        with open(CLIENT_TABLE,mode='r') as f:
                reader = csv.DictReader(f,fieldnames=CLIENT_SCHEMA)
                for row in reader:
                        clients.append(row)

def _save_client_to_storage():
        global clients
        tmp_table_name = '{}.tpm'.format(CLIENT_TABLE)
        with open(tmp_table_name,mode='w') as f:
                writer = csv.DictWriter(f,fieldnames=CLIENT_SCHEMA)
                writer.writerows(clients)
                os.remove(CLIENT_TABLE)
        
        os.rename(tmp_table_name,CLIENT_TABLE)

def create_client(name_client):
        global clients
        if name_client not in clients:
                #_add_comma()
                clients.append(name_client)
        else:
                print('the name already exists')

def _add_comma():
        global clients
        if len(clients)>0:
                clients += ','


def _update_client(client__name_old,client_new):
        global clients
        index = _search_client_index(client__name_old,'name')
        if index >= 0:
                clients[index]['name'] = client_new['name']
                clients[index]['company'] = client_new['company']
                clients[index]['email'] = client_new['email']
                clients[index]['position'] = client_new['position']

        # if name_client in clients:
        #         idx  = clients.index(name_client)
        #         clients[idx] = update_client_name
                #clients = clients.replace(name_client,update_client_name)
        else:
            _message_client_no_exits()
def _delete_client(name_client):
        global clients
        # for item in clients:
        #         keyItem = item.get(name_client,None)
        #         if not keyItem:
        #                 break
        exists_client = False
        for client in clients:
                if client['name'].upper() == name_client.upper():
                        exists_client = True
                        clients.remove(client)
                #clients =  clients.replace(name_client,"")            
        if exists_client == False:
                _message_client_no_exits()
        #_valid_twice_comma()

def _search_client(name_client):
        global clients
        for i in clients:
                if i == name_client:
                        return True

def _search_client_index(client_value,client_field):
        global clients
        for idx,client in enumerate(clients):
                if client[client_field].upper() == client_value.upper():
                        return idx
        return -1

def  _valid_twice_comma():
        """Valid comma alone"""
        global clients
        caracter_replace = ','
        clients = clients.replace(caracter_replace * 2,caracter_replace)
        if clients.startswith(caracter_replace):
                clients = clients[1::]
        if clients.endswith(caracter_replace):
                clients = clients[0:-1]

def _message_client_no_exits():
        print('the client\'s name no exits.')    

def _get_client_name():
        client_name = None
        while not client_name :
                client_name=input('What is your client name:  ')
                if client_name == 'exit':
                        sys.exit()
        return client_name

def _get_client_field(field_name):
        client_field = None
        while not client_field :
                client_field=input('What is your client {}?:  '.format(field_name))
                if client_field == 'exit':
                        sys.exit()
        return client_field

def _get_client_user():
        client_name = None
        client_email = None
        client_company = ""
        client_position = ""
        while not client_name and not client_email:
                
                client_name=_get_client_field('name')
                client_company=_get_client_field('compamy')
                client_email=_get_client_field('email')
                client_position=_get_client_field('position')

                if client_name == 'exit':
                        sys.exit()

        return {
                'name' : client_name,
                'company' : client_company,
                'email' : client_email,
                'position' : client_position
        }


def _list_clients():
        global clients
        for idx, client in enumerate(clients):        
                # print('{}: {}'.format(idx,client["name"]) )
                print('{uid} | {name} | {company} | {email} | {position}'.format(
                        uid = idx,  
                        name = client['name'],
                        company = client['company'],
                        email = client['email'],
                        position = client['position']
                        ))

def _print_welcome():
        print('WELCOME TO JOHN SALES')
        print('*' * 50)
        print('What would you like to do today?')
        print('[C]reate client')
        print('[D]elete client')
        print('[U]pdate client')
        print('[S]earch client')
        print('[L]list client')

if __name__ == '__main__':
        _inicializa_clients_from_storage()
        _print_welcome()
        command = input().upper()
        
        if command == 'C':
                client=_get_client_user()
                create_client(client)
        elif command == 'D':
                client_name = _get_client_name()
                _delete_client(client_name)
        elif command =='U':
                client_name=_get_client_name()
                print('Write your new client\'s values')
                client_new = _get_client_user()
                _update_client(client_name,client_new)
        elif command =='S':
                client_name = _get_client_name()
                found_client = _search_client_index(client_name,'name')
                if found_client:
                        print('The client ' + client_name + ' exists ')
                else:
                        print('The client ' + client_name + ' not exists ')
        elif command == 'L':
                _list_clients()

        else:
                print('Invalid command')

        _save_client_to_storage()