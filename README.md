AntSocks(for study only)

  A simple sockes5 proxy. Include a server and a client. The Client is the local proxy server for browsers or apps. The server is the outer-world's gate deploy on anywhere.
  The network traffic beteen server and client is encrypted by AES. The secret key is pre-defined in .conf file(See in .conf file issues). The secret iv is random generated in every client-server handshake. .

------------------------------
Package needed:

  Crypto	Python encrypt module. pycryptodome is recommended. Crypto is also working. I've packed the module in / path.

------------------------------
Server: AntSocksDemon

  The AntSocks server. Touch the outer-world's gate actually.
  It can be deployed in Liunx Platform. And Need Python 3.6 and above.
  
  ./startup.sh		Startup the server as a backgroud process.

  ./stop.sh		Stop the server. Just kill the server.

  antsocksd.py          Main entrance for server. Can be run by python3. Use -h or nothing for help.

  antsocksd.conf	Conf file for server.

    [TCP_Listener]	Server tcp listener section.
      tcp_listener = True	Enable tcp listerer by default. Mmmmmmm... Change this will cause crash...
      tcp_listen_ip = 0.0.0.0	Listener ip. Default is listen all ip.
      tcp_listen_port = 9999	Listener port. Change this value is recommended.
    [Server]		Server common section.
      server_name = Server1	Server name. Up to 16 characters.
    [Encrypt]		Encrypt section.
      encrypt_key = 78f41f2c57efa727a4be179049cecf89	Pre-Defined secret-key. Should be same as client. 32 characters and numbers only. Recommend to change. 

-------------------------------
Client: AntSocks

  The AntSocks client. The local proxy server for browser or other apps.
  It can be deployed in Liunx Platform. And Need Python 3.6 and above. Windows... Some strange issue in windows platform. So... To be continued.

  ./startup.sh          Startup the client as a backgroud process.

  ./stop.sh             Stop the client. Just kill the client.

  antsocks.py          	Main entrance for client. Can be run by python3. Use -h or nothing for help.

  antsocks.conf        Conf file for client.

    [Remote_Server]	AntSocks server section.
      tcp_conn = True		Enable tcp listerer by default. Mmmmmmm... Change this will cause crash...
      tcp_server_ip = localhost	Server's ip address. Change to actual address.
      tcp_server_port = 9999	Server's port. Change to actual port.
    [Local_TCP_Listener]	Local listener section. For browsers or apps uses.
      tcp_listener = True	Enable tcp listerer by default. Mmmmmmm... Change this will cause crash...
      tcp_listen_ip = 0.0.0.0   Listener ip. Default is listen all ip.
      tcp_listen_port = 8989    Listener port. 
    [Client_Name]
      client_name = client1	Client name. Up to 16 characters.
    [Encrypt]           Encrypt section.
      encrypt_key = 78f41f2c57efa727a4be179049cecf89    Pre-Defined secret-key. Should be same as server. 32 characters and numbers only. Recommend to change.


