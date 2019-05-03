from sshtunnel import SSHTunnelForwarder


class Tunnel():
    def __init__(self):
        self.server = None

    def start_tunnel(self, private_server_url, ssh_username, ssh_pkey, gateway_url, local_url):
        self.stop_tunnel()
        gateway_url = gateway_url.split(':')
        private_server = private_server_url.split(':')
        if len(private_server) < 2:
            raise Exception("Server Port Not Specified")
        if len(gateway_url) < 2:
            raise Exception("Gateway Port Not Specified")
        local = local_url.split(':')
        if len(local) < 2:
            raise Exception("Url Port Not Specified")
        self.server = SSHTunnelForwarder(
            (gateway_url[0], int(gateway_url[1])),
            ssh_username=ssh_username,
            ssh_pkey=ssh_pkey,
            remote_bind_address=(private_server[0], int(private_server[1])),
            local_bind_address=(local[0], int(local[1]))
        )
        self.server.start()

    def stop_tunnel(self):
        if self.server:
            self.server.stop()

    def __del__(self):
        self.stop_tunnel()
