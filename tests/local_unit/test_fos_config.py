from __future__ import absolute_import, division, print_function
__metaclass__ = type

import subprocess
import unittest
import re


Cli = 'ansible-playbook -i '
Inventory = '/home/cicd/inventory/inventory '
PlaybookPath = 'tests/local_unit/playbooks/fos_config/'


class Test(unittest.TestCase):

    def test_fos_config_no_change(self):
        command = Cli + Inventory + PlaybookPath + 'no_change.yaml -vvv'
        retcode, output = subprocess.getstatusoutput(command)
        if retcode:
            self.fail(output)
        else:
            self.assertNotEqual(output.find('changed=0'), -1)

    def test_fos_config_backup(self):
        retcode, output = subprocess.getstatusoutput('mkdir -p ~/pswitch')
        if retcode:
            self.fail(output)

        command = Cli + Inventory + PlaybookPath + 'backup.yaml -vvv'
        retcode, output = subprocess.getstatusoutput(command)
        if retcode:
            self.fail(output)

        retcode, output = subprocess.getstatusoutput('ls ~/pswitch | grep backup.cfg')
        if retcode:
            self.fail(output)
        else:
            self.assertEqual(output, 'backup.cfg')

        retcode, output = subprocess.getstatusoutput('rm -fr ~/pswitch')
        if retcode:
            self.fail(output)

    def test_fos_config_src(self):
        command = Cli + Inventory + PlaybookPath + 'src_1.yaml -vvv'
        retcode, output = subprocess.getstatusoutput(command)
        if retcode:
            self.fail(output)
        else:
            self.assertNotEqual(output.find('changed=1'), -1)

        command = Cli + Inventory + PlaybookPath + 'src_2.yaml -vvv'
        retcode, output = subprocess.getstatusoutput(command)
        if retcode:
            self.fail(output)
        else:
            self.assertNotEqual(output.find('changed=1'), -1)

        command = Cli + Inventory + PlaybookPath + 'src_2.yaml -vvv'
        retcode, output = subprocess.getstatusoutput(command)
        if retcode:
            self.fail(output)
        else:
            self.assertNotEqual(output.find('changed=0'), -1)


if __name__ == '__main__':
    unittest.main()
