import os
import subprocess

from ansible.module_utils.basic import AnsibleModule

# Ansible homebrew_cask task does not support a 'latest' state.

def is_present(name):
    installed = subprocess.check_output(
        ['brew', 'cask', 'list', '-1']).splitlines()
    return name in installed

def is_outdated(name):
    info = subprocess.check_output(['brew', 'cask', 'info', name]).splitlines()

    latest_version = info[0].split()[-1]
    installed_version = os.path.basename(info[2].split()[0])

    return latest_version != installed_version


def install(name):
    subprocess.check_call(['brew', 'cask', 'install', name])


def upgrade(name):
    return subprocess.check_output(['brew', 'cask', 'install', '--force', name])


def uninstall(name):
    subprocess.check_call(['brew', 'cask', 'uninstall', name])


def main():
    module = AnsibleModule(argument_spec=dict(
        state=dict(
            default='latest', choices=['latest', 'absent']),
        name=dict(required=True), ))

    state = module.params['state']
    name = module.params['name']

    if state == 'latest':
        if is_present(name):
            if (is_outdated(name)):
                upgrade(name)
                module.exit_json(changed=True)
            else:
                module.exit_json(changed=False)

        else:
            install(name)
            module.exit_json(changed=True)

    elif state == 'absent':
        if is_present(name):
            uninstall(name)
            module.exit_json(changed=True)
        else:
            module.exit_json(changed=False)


if __name__ == '__main__':
    main()
