import subprocess


class Tmux:
    def __init__(self, name, window=1, pane=1):
        self.session = name
        self.window = f'{self.session}:{window}'
        self.pane = f'{self.window}.{pane}'

    def build_session(self):
        print(f'Creating Session: {self.session}')
        subprocess.call(['tmux', 'new', '-d', '-s', self.session])

    def cmd_call(self, command):
        subprocess.call(['tmux', 'send-keys', '-t', self.pane, command, 'Enter'])

    def destroy_session(self):
        pass

    def verify_session(self):
        # TODO: Verify window and pane are valid too
        return subprocess.getstatusoutput(f'tmux ls | grep {self.session}')[0]

