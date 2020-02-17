import subprocess
import sys
import os
import json
import warnings
from threading import Timer


class GUITimeout(Exception):
    pass


class GUIProccessError(Exception):
    pass


class GUIPrompt(object):
    def __init__(self, title, button='OK', timeout=None):
        self.path = os.path.abspath(os.path.dirname(__file__))
        self.title = title
        self.button = button
        self.timeout = timeout
        self._pid = None
        self._timer_ended = False

    def script(self, fname):
        '''return full path to fname python script'''
        return os.path.join(self.path, fname)

    def _end_timer(self):
        self._timer_ended = True
        self.kill()

    def _kill_on_timeout(self, timeout):
        self._timer_ended = False
        err = 'Prompt timeout expired after {} seconds'.format(timeout)
        raise GUITimeout(err)

    def kill(self):
        try:
            self._pid.kill()
        except:
            warnings.warn('No killable process found')
        self._pid = None
        self._timedout = False

    def run(self, timeout, args, data=None):
        '''run args in a subprocess, sending data through stdin on an optional
        timer'''
        self._pid = subprocess.Popen(args,
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
        timer = Timer(timeout, self._end_timer)
        timer.start()
        try:
            stdout, stderr = self._pid.communicate(data)
            if stderr:
                warnings.warn(stderr)
            if self._pid and self._pid.returncode != 0:
                err = 'Prompt terminated unexpectedly with exit code {}'.format(
                    self._pid.returncode)
                raise GUIProccessError(err)
            return stdout.decode()
        finally:
            timer.cancel()
            if self._timer_ended:
                self._kill_on_timeout(timeout)
            else:
                self.kill()

    def notify(self, prompt, **kwargs):
        timeout = kwargs.get('timeout', self.timeout)
        args = [sys.executable, self.script('notify.py'),
                '--prompt', prompt]
        args.extend(['--title', kwargs.get('title', self.title)])
        args.extend(['--button', kwargs.get('button', self.button)])
        return self.run(timeout, args)

    def spinner(self, prompt, **kwargs):
        timeout = kwargs.get('timeout', self.timeout)
        args = [sys.executable, self.script('spinner.py'),
                '--prompt', prompt]
        args.extend(['--title', kwargs.get('title', self.title)])
        if timeout:
            try:
                _ = self.run(timeout, args)
            except GUITimeout:
                pass
        else:
            self._pid = subprocess.Popen(args)

    def two_button(self, prompt, button1, button2, **kwargs):
        timeout = kwargs.get('timeout', self.timeout)
        args = [sys.executable, self.script('two_button.py'),
                '--prompt', prompt,
                '--button1', button1,
                '--button2', button2]
        args.extend(['--title', kwargs.get('title', self.title)])
        return self.run(timeout, args)

    def line(self, prompt, **kwargs):
        timeout = kwargs.get('timeout', self.timeout)
        args = [sys.executable, self.script('singleline.py'),
                '--prompt', prompt]
        args.extend(['--title', kwargs.get('title', self.title)])
        args.extend(['--button', kwargs.get('button', self.button)])
        args.extend(['--default', kwargs.get('default', '')])
        return self.run(timeout, args)

    def open(self, prompt, **kwargs):
        timeout = kwargs.get('timeout', self.timeout)
        args = [sys.executable, self.script('picker.py'),
                '--prompt', prompt]
        args.extend(['--title', kwargs.get('title', self.title)])
        args.extend(['--button', kwargs.get('button', self.button)])
        args.extend(['--default', kwargs.get('default', '')])
        args.extend('--open')
        return self.run(timeout, args)

    def save(self, prompt, **kwargs):
        timeout = kwargs.get('timeout', self.timeout)
        args = [sys.executable, self.script('picker.py'),
                '--prompt', prompt]
        args.extend(['--title', kwargs.get('title', self.title)])
        args.extend(['--button', kwargs.get('button', self.button)])
        args.extend(['--default', kwargs.get('default', '')])
        args.extend('--save')
        return self.run(timeout, args)

    def multiline(self, prompt, **kwargs):
        timeout = kwargs.get('timeout', self.timeout)
        args = [sys.executable, self.script('multeline.py'),
                '--prompt', prompt]
        args.extend(['--title', kwargs.get('title', self.title)])
        args.extend(['--button', kwargs.get('button', self.button)])
        args.extend(['--default', kwargs.get('default', '')])
        return self.run(timeout, args)

    def credentials(self, prompt, **kwargs):
        timeout = kwargs.get('timeout', self.timeout)
        args = [sys.executable, self.script('credentials.py'),
                '--prompt', prompt]
        args.extend(['--title', kwargs.get('title', self.title)])
        args.extend(['--button', kwargs.get('button', self.button)])
        return json.loads(self.run(timeout, args))

    def list_select(self, prompt, list, **kwargs):
        timeout = kwargs.get('timeout', self.timeout)
        args = [sys.executable, self.script('listselect.py'),
                '--prompt', prompt,
                '--list', json.dumps(list)]
        args.extend(['--title', kwargs.get('title', self.title)])
        args.extend(['--button', kwargs.get('button', self.button)])
        return self.run(timeout, args)

    def table_select(self, prompt, table, multiple=False, **kwargs):
        timeout = kwargs.get('timeout', self.timeout)
        args = [sys.executable, self.script('tableselect.py'),
                '--prompt', prompt]
        args.extend(['--title', kwargs.get('title', self.title)])
        args.extend(['--button', kwargs.get('button', self.button)])
        if multiple:
            args.append('--multiple')
        data = json.dumps(table).encode()
        return json.loads(self.run(timeout, args, data))
