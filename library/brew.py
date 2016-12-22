import subprocess

from ansible.module_utils.basic import AnsibleModule


def is_present(name):
    installed = subprocess.check_output(['brew', 'list', '-1']).splitlines()
    return name in installed

def is_outdated(name):
    outdated = subprocess.check_output(['brew', 'outdated', '--quiet']).splitlines()
    return name in outdated

def install(name):
    subprocess.check_call(['brew', 'install', name])

def upgrade(name):
    subprocess.check_call(['brew', 'update', name])

def uninstall(name):
    subprocess.check_call(['brew', 'uninstall', name])


def main():
    module = AnsibleModule(
        argument_spec = dict(
            state     = dict(default='latest', choices=['latest', 'absent']),
            name      = dict(required=True),
        )
    )

    state = module.params['state']
    name = module.params['name']

    if state == 'latest':
        if is_present(name):
            if is_outdated(name):
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
