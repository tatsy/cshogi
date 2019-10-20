﻿import subprocess
import os.path
import locale

class Engine:
    def __init__(self, cmd, connect=True):
        self.cmd = cmd
        if connect:
            self.connect()
        else:
            self.proc = None
            self.name = None

    def connect(self):
        self.proc = subprocess.Popen([self.cmd], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.path.dirname(self.cmd))

        self.proc.stdin.write(b'usi\n')
        self.proc.stdin.flush()

        while True:
            self.proc.stdout.flush()
            line = self.proc.stdout.readline().strip()
            if line[:7] == b'id name':
                self.name = line[8:].decode('ascii')
            elif line == b'usiok':
                break
        print(self.name)

    def usi(self):
        cmd = 'usi'
        print(cmd)
        self.proc.stdin.write(cmd.encode('ascii') + b'\n')
        self.proc.stdin.flush()

        while True:
            self.proc.stdout.flush()
            line = self.proc.stdout.readline().strip().decode(locale.getpreferredencoding())
            print(line)
            if line == 'usiok':
                break

    def setoption(self, name, value):
        cmd = 'setoption name ' + name + ' value ' + str(value)
        print(cmd)
        self.proc.stdin.write(cmd.encode(locale.getpreferredencoding()) + b'\n')
        self.proc.stdin.flush()

    def isready(self):
        cmd = 'isready'
        print(cmd)
        self.proc.stdin.write(cmd.encode('ascii') + b'\n')
        self.proc.stdin.flush()

        while True:
            self.proc.stdout.flush()
            line = self.proc.stdout.readline().strip().decode('ascii')
            print(line)
            if line == 'readyok':
                break

    def usinewgame(self):
        cmd = 'usinewgame'
        print(cmd)
        self.proc.stdin.write(cmd.encode('ascii') + b'\n')
        self.proc.stdin.flush()

    def position(self, moves=None, sfen="startpos"):
        cmd = 'position ' + sfen
        if moves:
            cmd += ' moves ' + ' '.join(moves)
        print(cmd)
        self.proc.stdin.write(cmd.encode('ascii') + b'\n')
        self.proc.stdin.flush()

    def go(self, ponder=False, btime=None, wtime=None, byoyomi=None, binc=None, winc=None):
        cmd = 'go'
        if ponder:
            cmd += ' ponder'
        else:
            if btime is not None:
                cmd += ' btime ' + str(btime)
            if wtime is not None:
                cmd += ' wtime ' + str(wtime)
            if byoyomi is not None:
                cmd += ' byoyomi ' + str(byoyomi)
            else:
                if binc is not None:
                    cmd += ' binc ' + str(binc)
                if winc is not None:
                    cmd += ' winc ' + str(winc)
        print(cmd)
        self.proc.stdin.write(cmd.encode('ascii') + b'\n')
        self.proc.stdin.flush()

        while True:
            self.proc.stdout.flush()
            line = self.proc.stdout.readline().strip().decode('ascii')
            print(line)
            if line[:8] == 'bestmove':
                items = line[9:].split(' ')
                if len(items) == 3 and items[1] == 'ponder':
                    return items[0], items[2]
                else:
                    return items[0], None

    def quit(self):
        self.proc.stdin.write(b'quit\n')
        self.proc.stdin.flush()
        self.proc.wait()
        self.proc = None