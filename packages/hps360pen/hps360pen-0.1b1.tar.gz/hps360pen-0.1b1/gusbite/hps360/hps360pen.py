import collections
import click
import evdev as evd

HP_ELAN_PEN = "ELAN2514:00 04F3:280E"
Device = collections.namedtuple('Device', ('id', 'name', 'evdev'))


@click.command()
@click.option('--list', 'select_from_list', is_flag=True, default=False, required=False,
              help="List event devices and prompt for a device selection. Otherwise, default HP PEN signature "
                   "will be used.")
def hps360pen(select_from_list: bool):
    """
    hps360pen is a sample tool to map HP Spectre x360 ap00xxxx stock pen buttons.

    For now, only the pen's bottom button is supported and is mapped to emulate the right mouse button.
    """
    devices = [evd.InputDevice(path) for path in evd.list_devices()]
    devices = [Device(id=idx, name=device.name, evdev=device) for idx, device in enumerate(devices)]

    if select_from_list:

        click.echo(message="Select the HP PEN device from the the list below")

        for device in devices:
            click.echo(f"[{device.id}] - '{device.name}'")

        selection = click.prompt(text='Your selection', type=click.IntRange(min=0, max=len(list(devices))-1), )

        device = devices[selection]
    else:
        click.echo(message="Looking for default HP ELAN PEN signature...")
        for dev in devices:
            if dev.name == HP_ELAN_PEN:
                device = dev
                break
        else:
            click.echo(message=f"Unable to find '{HP_ELAN_PEN}' event device.")
            return -1

    click.echo(message=f"Listening events for input device '{device.name} at '{device.evdev.path}'")

    capabilities = {  # evdev input capabilities for simulating mouse click
        evd.ecodes.EV_KEY: (evd.ecodes.BTN_LEFT, evd.ecodes.BTN_RIGHT, evd.ecodes.BTN_MIDDLE),
    }

    with evd.UInput(capabilities) as ui:
        for event in device.evdev.read_loop():
            if event.code == 321:  # BTN_PEN_BOTTOM
                ui.write(evd.ecodes.EV_KEY, evd.ecodes.BTN_RIGHT, event.value)
                ui.syn()
            elif event.code == 331:  # BTN_PEN_UPPER
                pass


if __name__ == "__main__":
    hps360pen()
