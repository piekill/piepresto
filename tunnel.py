from sshtunnel import SSHTunnelForwarder
from timeout import timeout


class Tunnel():
    def __init__(self):
        self.server = None

    @timeout(6, "Fail to establish tunnel")
    def start_tunnel(
            self, private_server_url, gateway_url, ssh_username, use_keyfile,
            ssh_pkey, ssh_pwd, local_url):
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

        if use_keyfile:
            self.server = SSHTunnelForwarder(
                (gateway_url[0], int(gateway_url[1])),
                ssh_username=ssh_username,
                ssh_pkey=ssh_pkey,
                remote_bind_address=(private_server[0], int(private_server[1])),
                local_bind_address=(local[0], int(local[1]))
            )
        else:
            self.server = SSHTunnelForwarder(
                (gateway_url[0], int(gateway_url[1])),
                ssh_username=ssh_username,
                ssh_password=ssh_pwd,
                remote_bind_address=(private_server[0], int(private_server[1])),
                local_bind_address=(local[0], int(local[1]))
            )
        self.server.start()

    def stop_tunnel(self):
        if self.server:
            self.server.stop()

    def __del__(self):
        self.stop_tunnel()
