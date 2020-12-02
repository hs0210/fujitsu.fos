import subprocess
import unittest


Cli = 'ansible-playbook -i '
Inventory = '/home/cicd/inventory/inventory '
PlaybookPath = 'tests/local_unit/playbooks/fos_command/'

class Test(unittest.TestCase):
    def test_fos_command_simple(self):
        command = Cli + Inventory + PlaybookPath + 'show_version.yaml -vvv | grep "Current Runtime Version"'
        retcode, output = subprocess.getstatusoutput(command)
        self.assertEqual(retcode, 0)
        self.assertIn('Current Runtime Version', output)

    def test_fos_command_wait_for(self):
        command = Cli + Inventory + PlaybookPath + 'wait_for.yaml -vvv | grep "Current Runtime Version"'
        retcode, output = subprocess.getstatusoutput(command)
        self.assertEqual(retcode, 0)
        self.assertIn('Current Runtime Version', output)

    def test_fos_command_wait_for_fails(self):
        command = Cli + Inventory + PlaybookPath + 'wait_for_fail.yaml -vvv | grep "Current Runtime Version"'
        retcode, output = subprocess.getstatusoutput(command)
        self.assertNotEqual(retcode, 0)
        self.assertNotIn('Current Runtime Version', output)

    def test_fos_command_match_any(self):
        command = Cli + Inventory + PlaybookPath + 'match_any.yaml -vvv | grep "Current Runtime Version"'
        retcode, output = subprocess.getstatusoutput(command)
        self.assertEqual(retcode, 0)
        self.assertIn('Current Runtime Version', output)

    def test_fos_command_match_all(self):
        command = Cli + Inventory + PlaybookPath + 'match_all.yaml -vvv | grep "Current Runtime Version"'
        retcode, output = subprocess.getstatusoutput(command)
        self.assertNotEqual(retcode, 0)
        self.assertNotIn('Current Runtime Version', output)


if __name__ == '__main__':
    unittest.main()
