import subprocess
import json


class Ansi():
    def __init__(self, play):
        self.play = play

    def run(self, payload):
        user = []
        extra_vars="--extra-vars={0}".format(json.dumps(payload))
        print extra_vars
        yaml = 'app/core/ansible/playbooks/{0}.yml'.format(self.play)
        command = [
                'ansible-playbook',
                '-i',
                'app/core/ansible/playbooks/inventory/hosts',
                extra_vars,
                yaml,
                '-vvvv'
                ]
        #cmd = ['ansible', 'all', '-m', 'setup']
        #for cmd in command[0]:
        #    user.append(cmd)
        #print cmd
        #print user
        execute = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                )
        output, error = execute.communicate()
        print output
        print error
        return output
