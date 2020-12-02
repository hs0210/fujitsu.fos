import subprocess
import unittest
import re


Cli = 'ansible-playbook -i '
Inventory = '/home/cicd/inventory/inventory '
PlaybookPath = 'tests/local_unit/playbooks/fos_facts/'

class Test(unittest.TestCase):
    def test_fos_facts_gather_subset_default(self):
        command = Cli + Inventory + PlaybookPath + 'gather_subset_default.yaml -vvv'
        retcode, output = subprocess.getstatusoutput(command)
        self.assertEqual(retcode, 0)
        ansible_net_gather_subset = re.findall(r'ansible_net_gather_subset(.+?)],', output, re.S)
        self.assertIn('default', str(ansible_net_gather_subset))
        ansible_net_runtime_version = re.findall(r'ansible_net_runtime_version(.+?),', output, re.S)
        self.assertIn('1.3.67', str(ansible_net_runtime_version))
        ansible_net_bootloader_version = re.findall(r'ansible_net_bootloader_version(.+?),', output, re.S)
        self.assertIn('1.0.0', str(ansible_net_bootloader_version))
        ansible_net_hostname = re.findall(r'ansible_net_hostname(.+?),', output, re.S)
        self.assertIn('admin', str(ansible_net_hostname))

    def test_fos_facts_gather_subset_config(self):
        command = Cli + Inventory + PlaybookPath + 'gather_subset_config.yaml -vvv'
        retcode, output = subprocess.getstatusoutput(command)
        # print(output)
        self.assertEqual(retcode, 0)
        ansible_net_gather_subset = re.findall(r'ansible_net_gather_subset(.+?)],', output, re.S)
        self.assertIn('default', str(ansible_net_gather_subset))
        self.assertIn('config', str(ansible_net_gather_subset))
        ansible_net_hostname = re.findall(r'ansible_net_hostname(.+?),', output, re.S)
        self.assertIn('admin', str(ansible_net_hostname))
        self.assertIn('ansible_net_config', output)

    def test_fos_facts_gather_subset_hardware(self):
        command = Cli + Inventory + PlaybookPath + 'gather_subset_hardware.yaml -vvv'
        retcode, output = subprocess.getstatusoutput(command)
        self.assertEqual(retcode, 0)
        ansible_net_gather_subset = re.findall(r'ansible_net_gather_subset(.+?)],', output, re.S)
        self.assertIn('default', str(ansible_net_gather_subset))
        self.assertIn('hardware', str(ansible_net_gather_subset))
        ansible_net_memtotal_mb = re.findall(r'ansible_net_memtotal_mb(.+?),', output, re.S)
        self.assertIn('3949', str(ansible_net_memtotal_mb))
        ansible_net_model = re.findall(r'ansible_net_model(.+?),', output, re.S)
        self.assertIn('ET-7648BRA-FOS', str(ansible_net_model))
        ansible_net_burned_in_mac = re.findall(r'ansible_net_burned_in_mac(.+?),', output, re.S)
        self.assertIn('00:30:AB:F4:CA:DA', str(ansible_net_burned_in_mac))



if __name__ == '__main__':
    unittest.main()
