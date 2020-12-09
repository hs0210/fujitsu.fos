# (c) 2020 Red Hat, Inc
#
#
# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re
import json

from ansible.module_utils._text import to_text
from ansible.module_utils.connection import Connection, ConnectionError
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import to_list
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.config import NetworkConfig

_DEVICE_CONFIGS = {}


def get_config(module, flags=None):
    flags = to_list(flags)

    flag_str = ' '.join(flags)

    try:
        return _DEVICE_CONFIGS[flag_str]
    except KeyError:
        connection = get_connection(module)
        try:
            out = connection.get_config(flags=flags)
        except ConnectionError as exc:
            module.fail_json(msg=to_text(exc, errors='surrogate_then_replace'))
        cfg = to_text(out, errors='surrogate_then_replace').strip()
        _DEVICE_CONFIGS[flag_str] = cfg
        return cfg


def run_commands(module, commands, check_rc=True):
    responses = list()
    connection = get_connection(module)

    for cmd in to_list(commands):
        if isinstance(cmd, dict):
            command = cmd['command']
            prompt = cmd['prompt']
            answer = cmd['answer']
        else:
            command = cmd
            prompt = None
            answer = None

        try:
            out = connection.get(command, prompt, answer)
            out = to_text(out, errors='surrogate_or_strict')
        except ConnectionError as exc:
            module.fail_json(msg=to_text(exc))
        except UnicodeError:
            module.fail_json(msg=u'Failed to decode output from %s: %s' % (cmd, to_text(out)))

        responses.append(out)

    return responses


def get_connection(module):
    if hasattr(module, '_fos_connection'):
        return module._fos_connection

    module._fos_connection = Connection(module._socket_path)

    return module._fos_connection


def get_defaults_flag(module):
    connection = get_connection(module)
    try:
        out = connection.get_defaults_flag()
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc, errors='surrogate_then_replace'))
    return to_text(out, errors='surrogate_then_replace').strip()


def send_data(module, data):
    connection = Connection(module._socket_path)
    if (connection):
        try:
            connection.send_data(data=data)
        except ConnectionError as exc:
            module.fail_json(msg=to_text(exc))


def load_config(module, commands):
    connection = get_connection(module)

    try:
        resp = connection.edit_config(commands)
        return resp.get('response')
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc))

def is_parents(command):
    parents_set = ['interface', 'router']
    for val in parents_set:
        if command.startswith(val):
            return True
        else:
            return False

def load_running_config(running):
    running_obj = NetworkConfig(indent=4)
    running = running.strip().split('\n')

    index = 0
    while index < len(running):
        if is_parents(running[index]):
            parents = running[index] + '\n'
            parents = parents.strip().split('\n')
            children = list()
            i = index + 1
            while i < len(running) and running[i] != 'exit' and running[i] != '':
                children.append(running[i])
                i += 1
            if i < len(running) and running[i] != '':
                children.append(running[i])
            index = i
            running_obj.add(children, parents)
        else:
            line = running[index] + '\n'
            line = line.strip().split('\n')
            running_obj.add(list(), line)
        index += 1

    return running_obj