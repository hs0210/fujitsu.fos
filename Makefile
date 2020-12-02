test:
	@python3 tests/local_unit/test_fos_command.py
	@python3 tests/local_unit/test_fos_facts.py
	@python3 tests/local_unit/test_fos_config.py

playbook:
	@ansible-playbook -i /home/cicd/inventory/inventory tests/local_unit/playbooks/playbook.yaml -vvv

copy:
	@mkdir -p ~/.ansible/collections/ansible_collections/fujitsu/fos/
	@cp -r plugins/ ~/.ansible/
	@cp -r plugins/ ~/.ansible/collections/ansible_collections/fujitsu/fos/
