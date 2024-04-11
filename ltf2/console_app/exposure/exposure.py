import os
import subprocess
import time


class BaseExposure:
    def __init__(self, shell=False):
        self.handle = None
        self.cmd_line = None
        self.shell = shell

    def start(self):
        cmd = self.cmd_line if self.shell else self.cmd_line.split()
        print('>>>> cmd:', cmd)
        self.handle = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=self.shell,
            preexec_fn=os.setpgrp)
        print('>>>> handle pid:', self.handle.pid)

    def stop(self):
        if not self.handle:
            return
        max_killing_tries = 5
        while max_killing_tries > 0:
            # subprocess.call(f'sudo kill -2 {self.handle.pid}'.split())
            subprocess.call(f'sudo pkill -TERM -P {self.handle.pid}'.split())
            if self.handle.poll() is None:
                max_killing_tries -= 1
                time.sleep(1)
                continue
            self.handle = None
            break
        else:
            raise Exception(f'The pid {self.handle.pid} was not killed in {max_killing_tries}s')


class NcExposure(BaseExposure):
    def __init__(self, port):
        super().__init__()
        self.port = port
        self.cmd_line = f'sudo nc -lk {port}'

    def __repr__(self):
        return f'NcExposure port: {self.port}, active: {self.handle is not None}'


class HttpExposure(BaseExposure):
    def __init__(self, port, tls=False):
        super().__init__(shell=True)
        self.port = port
        cwd = os.getcwd()
        self.tls_name = tls
        path_pref = f'{cwd}/ltf2/console_app/exposure'
        self.tls = f'{path_pref}/certs/{tls}.pem' if tls else ''
        self.cmd_line = f'sudo python3 {path_pref}/http_serv.py -p {port} -tls "{self.tls}"'

    def __repr__(self):
        return f'HttpExposure port: {self.port}, TLS: {self.tls_name}, active: {self.handle is not None}'
