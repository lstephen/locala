import subprocess

from ansible.module_utils.basic import AnsibleModule


def is_present(name):
    installed = subprocess.check_output(
        ['brew', 'cask', 'list', '-1']).splitlines()
    return name in installed


def install(name):
    subprocess.check_call(['brew', 'cask', 'install', name])


def upgrade(name):
    return subprocess.check_output(['brew', 'cask', 'update', name])


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
            result = upgrade(name)

            changed = 'Already up-to-date.' not in result
            module.exit_json(changed=changed)

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
