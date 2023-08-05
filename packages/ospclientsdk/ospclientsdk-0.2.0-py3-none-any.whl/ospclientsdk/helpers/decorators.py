"""
    helpers.decorators

    The decorator that contains the logic for executing the
    openstack cli commands.

"""

import os
import json
import subprocess
from logging import getLogger
from string import Template
from functools import update_wrapper

LOG = getLogger(__name__)


class Command(object):
    """
    Command is a class decorator that handles the underlying functionality
    of executing the openstack commands locally through subprocess. This makes
    it easier to add future api commands that reflect the cli without repeating
    this logic code in the mixin classes.
    """

    generic_os_command_template = Template("openstack $command $options")

    def __init__(self, func):
        update_wrapper(self, func)
        self.function = func

    def __call__(self, *args, **kwargs):
        """
        This is the brains of the class that get's called when a decorated
        :param args:
        :param kwargs:
        :return:
        """
        self.function(*args, **kwargs)
        func_name = self.function.__name__

        # This means function declared in one of the command group mixins was called
        # because only commmand options parameter is passed. The idea
        # is we infer the command requested based on the function executed. i.e.
        # the 'server_create(options)' function would normalize and map to 'server create'
        # on the CLI.
        if len(args) == 2 and func_name.find('raw') == -1:
            return self.run_cmd(func_name, args[1])

        # Assume the user is trying has called the run_raw_command function to pass in a raw
        # string of an openstack command. Either because there is an api call that
        # maps to a CLI command or a particular option and it's argument can't/hasn't been
        # normalized yet.
        elif len(args) == 2 and func_name.find('raw') != -1:
            return self.run_cmd_raw(args[1])

        # This means run_command function in shell implementation is called because
        # user passes in the cmd as a parameter. Most likely because one of the command
        # mixin classes does not have a defined function yet that maps to a particular
        # command on the CLI.
        elif len(args) == 3:
            return self.run_cmd(args[1], args[2])

    def __get__(self, instance, owner):
        # Refer to the second answer on why I added this
        # so I can implement the descriptor protocol
        # https://stackoverflow.com/questions/2365701/decorating-python-class-methods-how-do-i-pass-the-instance-to-the-decorator
        from functools import partial
        return partial(self.__call__, instance)

    def run_cmd(self, cmd, options):
        """
        This is a higher level api command, that is used to normalize and
        join the final command to it options and parameters.

        :param cmd: str
        :param options: dict
        :return: str
        """
        opts = self._normalize_options(options)
        cmd = cmd.replace('_', ' ')
        if len(set(cmd.split(' ')).intersection(['create', 'list', 'show'])) != 0 and opts.find('--help') == -1:
            opts += ' -f json'
        cmd_str = self.generic_os_command_template.safe_substitute(command=cmd, options=opts)
        return self.run_cmd_raw(cmd_str)

    def run_cmd_raw(self, command):
        """
        This is a lower level api command meant to pass the full
        joined cli command with it's options

        :param command: str
        :return: str
        """
        LOG.debug('command: %s' % command)
        resp = self.exec_local_cmd(command)

        # if resp['stdout']:
        try:
            # Let's try to deserialize into a dictionary for easier manipulation
            data = json.loads(resp['stdout'])
            resp['stdout'] = data
            return resp
        except Exception:
            # assume it's not a json so just return the output
            return resp

    def _normalize_options(self, options):
        """
        This takes the dictionary representation of cli command arguments and options
        and normalizes it into their respective format. Example

        This dictionary of arguments/options for 'server create'

        dict(image='rhel-7.5-server-x86_64',
                flavor='m1.small',
                network=['provider_net', 'private_net'],
                max=2,
                key_name='test-key')

        is converted to:

        --image rhel-7.4-server-x86_64
        --flavor m1.small
        --network private_net
        --network provider_net
        --key-name test-key
        test_client


        :param options: dict
        :return: str
        """
        cmd_str = ""
        if isinstance(options, dict):
            asset = options.pop('name') if options.get('name', None) else options.pop('id', None)
            for key, val in options.items():
                if isinstance(val, list):
                    for item in val:
                        if isinstance(item, dict):
                            opt_list = ["=".join([k.replace('_', '-'), str(v)]) for k, v in item.items()]
                            if len(opt_list) > 1:
                                opt_list = ",".join(opt_list)
                            else:
                                opt_list = opt_list[-1]
                            cmd_str += "--%s %s " % (key.replace('_', '-'), opt_list)
                            continue
                        cmd_str += "--%s %s " % (key.replace('_', '-'), item)
                    continue
                if isinstance(val, bool):
                    cmd_str += "--%s " % key.replace('_', '-')
                    continue
                if isinstance(val, str):
                    if os.path.isdir(val) or os.path.isfile(val):
                        val = os.path.abspath(val)
                    if os.path.sep in val and not os.path.isfile(val):
                        val = os.path.abspath(val)
                    cmd_str += "--%s %s " % (key.replace('_', '-'), val)
                    continue
                cmd_str += "--%s %s " % (key.replace('_', '-'), val)
            if asset:
                cmd_str += asset
        return cmd_str

    def exec_local_cmd(self, cmd):
        """Execute command locally.

        :param cmd: str
        :return: dict
        """
        proc = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output = proc.communicate()
        resp = dict()
        resp['rc'] = proc.returncode
        resp['stdout'] = output[0].decode('utf-8')
        resp['stderr'] = output[1].decode('utf-8')
        return resp
