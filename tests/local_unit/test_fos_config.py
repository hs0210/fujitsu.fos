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
        command = Cli + Inventory + PlaybookPath + 'no_change.yaml -vvv | grep "changed=0"'
        retcode, output = subprocess.getstatusoutput(command)
        self.assertEqual(retcode, 0)
        self.assertIn('changed=0', output)

    def test_fos_config_backup(self):
        retcode, output = subprocess.getstatusoutput('mkdir -p ~/pswitch')
        self.assertEqual(retcode, 0)
        command = Cli + Inventory + PlaybookPath + 'backup.yaml -vvv'
        retcode, output = subprocess.getstatusoutput(command)
        self.assertEqual(retcode, 0)
        retcode, output = subprocess.getstatusoutput('ls ~/pswitch | grep backup.cfg')
        self.assertEqual(retcode, 0)
        self.assertEqual(output, 'backup.cfg')
        retcode, output = subprocess.getstatusoutput('rm -fr ~/pswitch')
        self.assertEqual(retcode, 0)

    def test_fos_config_src(self):
        command = Cli + Inventory + PlaybookPath + 'src_1.yaml -vvv | grep "changed=1"'
        retcode, output = subprocess.getstatusoutput(command)
        self.assertEqual(retcode, 0)
        self.assertIn('changed=1', output)

        command = Cli + Inventory + PlaybookPath + 'src_2.yaml -vvv | grep "changed=1"'
        retcode, output = subprocess.getstatusoutput(command)
        self.assertEqual(retcode, 0)
        self.assertIn('changed=1', output)

        command = Cli + Inventory + PlaybookPath + 'src_2.yaml -vvv | grep "changed=0"'
        retcode, output = subprocess.getstatusoutput(command)
        self.assertEqual(retcode, 0)
        self.assertIn('changed=0', output)


if __name__ == '__main__':
    unittest.main()
