from __future__ import absolute_import, division, print_function
__metaclass__ = type

import subprocess
import unittest
import re


Cli = 'ansible-playbook -i '
Inventory = '/home/cicd/inventory/inventory '
PlaybookPath = 'tests/local_unit/playbooks/fos_config/'

class Test(unittest.TestCase):

    # def test_fos_config_no_change(self):
    #     command = Cli + Inventory + PlaybookPath + 'no_change.yaml -vvv'
    #     retcode, output = subprocess.getstatusoutput(command)
    #     self.assertEqual(retcode, 0)
    #     print(output)

    def test_fos_config_backup(self):
        retcode, output = subprocess.getstatusoutput('mkdir -p /home/cicd/pswitch')
        self.assertEqual(retcode, 0)
        command = Cli + Inventory + PlaybookPath + 'backup.yaml -vvv'
        retcode, output= subprocess.getstatusoutput(command)
        self.assertEqual(retcode, 0)
        retcode, output = subprocess.getstatusoutput('ls /home/cicd/pswitch | grep backup.cfg')
        self.assertEqual(retcode, 0)
        self.assertEqual(output, 'backup.cfg')
        retcode, output = subprocess.getstatusoutput('rm -fr /home/cicd/pswitch')
        self.assertEqual(retcode, 0)
    
    # def test_fos_config_src(self):
    #     command = Cli + Inventory + PlaybookPath + 'src.yaml -vvv'
    #     retcode, output = subprocess.getstatusoutput(command)
    #     self.assertEqual(retcode, 0)
    #     print(output)

        # lines = ['hostname admin']
    #     args = dict(lines=lines)
    #     set_module_args(args)

    #     self.conn.get_diff = MagicMock(
    #         return_value=self.cliconf_obj.get_diff('\n'.join(lines), self.running_config)
    #     )
    #     self.execute_module()

    # def test_fos_config_src(self):
    #     src = load_fixture('fos_config', 'candidate.cfg')
    #     args = dict(src=src)
    #     set_module_args(args)

    #     self.conn.get_diff = MagicMock(
    #         return_value=self.cliconf_obj.get_diff(src, self.running_config)
    #     )
    #     config = [
    #         'hostname switch01',
    #         'interface Ethernet1',
    #         'description test interface',
    #         'no shutdown',
    #         'ip routing',
    #     ]
    #     self.execute_module(changed=True, commands=config)

    # def test_fos_config_lines(self):
    #     lines = ['hostname switch01', 'ip domain-name eng.ansible.com']
    #     args = dict(lines=lines)
    #     set_module_args(args)

    #     self.conn.get_diff = MagicMock(
    #         return_value=self.cliconf_obj.get_diff(
    #             '\n'.join(lines), self.running_config
    #         )
    #     )
    #     config = ['hostname switch01']
    #     self.execute_module(changed=True, commands=config)

    # def test_fos_config_parents(self):
    #     lines = ['ip address 1.2.3.4/5', 'no shutdown']
    #     parents = ['interface Ethernet10']
    #     args = dict(lines=lines, parents=parents)
    #     candidate = parents + lines
    #     set_module_args(args)

    #     self.conn.get_diff = MagicMock(
    #         return_value=self.cliconf_obj.get_diff(
    #             '\n'.join(candidate), self.running_config
    #         )
    #     )
    #     config = [
    #         'interface Ethernet10',
    #         'ip address 1.2.3.4/5',
    #         'no shutdown',
    #     ]
    #     self.execute_module(changed=True, commands=config, sort=False)

    # def test_fos_config_before(self):
    #     lines = ['hostname switch01', 'ip domain-name eng.ansible.com']
    #     before = ['before command']
    #     args = dict(lines=lines, before=before)
    #     set_module_args(args)

    #     self.conn.get_diff = MagicMock(
    #         return_value=self.cliconf_obj.get_diff(
    #             '\n'.join(lines), self.running_config
    #         )
    #     )
    #     config = ['before command', 'hostname switch01']
    #     result = self.execute_module(changed=True, commands=config)
    #     self.assertEqual('before command', result['commands'][0])

    # def test_fos_config_after(self):
    #     lines = ['hostname switch01', 'ip domain-name eng.ansible.com']
    #     args = dict(lines=lines, after=['after command'])

    #     set_module_args(args)
    #     self.conn.get_diff = MagicMock(
    #         return_value=self.cliconf_obj.get_diff(
    #             '\n'.join(lines), self.running_config
    #         )
    #     )
    #     config = ['after command', 'hostname switch01']
    #     result = self.execute_module(changed=True, commands=config)
    #     self.assertEqual('after command', result['commands'][-1])

    # def test_fos_config_src_and_lines_fails(self):
    #     args = dict(src='foo', lines='foo')
    #     set_module_args(args)
    #     self.execute_module(failed=True)

    # def test_fos_config_match_exact_requires_lines(self):
    #     args = dict(match='exact')
    #     set_module_args(args)
    #     self.execute_module(failed=True)

    # def test_fos_config_match_strict_requires_lines(self):
    #     args = dict(match='strict')
    #     set_module_args(args)
    #     self.execute_module(failed=True)

    # def test_fos_config_replace_block_requires_lines(self):
    #     args = dict(replace='block')
    #     set_module_args(args)
    #     self.execute_module(failed=True)

    # def test_fos_config_backup_returns__backup__(self):
    #     args = dict(backup=True)
    #     set_module_args(args)
    #     result = self.execute_module()
    #     self.assertIn('__backup__', result)

    # def test_fos_config_save(self):
    #     set_module_args(dict(save=True))
    #     self.execute_module(changed=True)
    #     self.assertEqual(self.run_commands.call_count, 1)
    #     self.assertEqual(self.get_config.call_count, 0)
    #     self.assertEqual(self.load_config.call_count, 0)
    #     args = self.run_commands.call_args[0][1]
    #     self.assertDictContainsSubset({'command': 'copy system:running-config nvram:startup-config'}, args[0])

    # def test_fos_config_match_none(self):
    #     lines = ['hostname router']
    #     set_module_args(dict(lines=lines, match='none'))
    #     self.conn.get_diff = MagicMock(
    #         return_value=self.cliconf_obj.get_diff(
    #             '\n'.join(lines), self.running_config
    #         )
    #     )
    #     self.execute_module(changed=True, commands=lines)

    # def test_fos_config_match_none(self):
    #     lines = ['ip address 1.2.3.4/5', 'shutdown1']
    #     # parents = ['interface Ethernet10']
    #     set_module_args(dict(lines=lines, match='exact'))
    #     self.conn.get_diff = MagicMock(
    #         return_value=self.cliconf_obj.get_diff(
    #             '\n'.join(lines), self.running_config
    #         )
    #     )
    #     # commands = parents + lines
    #     self.execute_module(changed=True, commands=lines, sort=False)



if __name__ == '__main__':
    unittest.main()
