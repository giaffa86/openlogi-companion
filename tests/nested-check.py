# SPDX-License-Identifier: GPL-3.0-or-later.
import ast
import json
import os
from pathlib import Path
import subprocess
import time

def evaluate(expression):
    code = expression
    result = subprocess.run(['gdbus', 'call', '--session', '--dest', 'org.gnome.Shell', '--object-path', '/org/gnome/Shell',
                             '--method', 'org.gnome.Shell.Eval', code], capture_output=True, text=True, timeout=5)
    if result.returncode:
        raise RuntimeError(result.stderr)
    ok, value = ast.literal_eval(result.stdout.replace('(true,', '(True,', 1).replace('(false,', '(False,', 1))
    if not ok:
        raise RuntimeError(value)
    return json.loads(value)

for attempt in range(100):
    try:
        if evaluate("!!Main.extensionManager.lookup('openlogi-companion@giaffa86')?.stateObj?._indicator?._snapshot"):
            break
    except (RuntimeError, ValueError):
        pass
    time.sleep(.2)
else:
    print(Path(os.environ['SANDBOX'], 'shell.log').read_text())
    raise RuntimeError('Extension did not become ready')

for attempt in range(100):
    if evaluate('!Main.layoutManager._startingUp'):
        break
    time.sleep(.1)
evaluate('(()=>{Main.overview.hide();return true})()')
time.sleep(.5)

checks = 0
prefix = "Main.extensionManager.lookup('openlogi-companion@giaffa86').stateObj"
def run(body):
    return evaluate('(()=>{const extension=' + prefix + ';const i=extension._indicator;' + body + '})()')
def check(value, message):
    global checks
    assert value, message
    checks += 1

check(run('return i._rows.length') == 9, 'Inventory rows')
check(run('return i._rows.filter(r=>r.device.id==="duplicate").length') == 2, 'Duplicates preserved')
check(run('return i._rows.at(-1)._detail.text.includes("84")') is False, 'Offline percentage hidden')
run('i._button.menu.open();return true')
time.sleep(.3)
check(run('return i._button.menu.isOpen'), 'Menu opens')
check(run('return i._scroll.width') <= 416, 'Bounded list width')
check(run('return i._rows.every(r=>r.can_focus)'), 'Keyboard focusable rows')
check(run('return i._rows.every(r=>r.accessible_name.length>0)'), 'Accessible row names')
check(run('return i._timer>0'), 'Polling enabled by menu open without preference')
check(run('return i._delay===5'), 'Menu poll is the fast interval')
# Live refresh with the menu open: no preference change, only the backend inventory.
inventory = Path(os.environ['SANDBOX'], 'bin/inventory.json')
fixture = json.loads(inventory.read_text())
trimmed = json.loads(json.dumps(fixture))
trimmed['data']['devices'] = trimmed['data']['devices'][:3]
inventory.write_text(json.dumps(trimmed))
for attempt in range(60):
    if run('return i._rows.length') == 3:
        break
    time.sleep(.25)
else:
    raise RuntimeError('Menu did not pick up a changed inventory')
check(True, 'Live refresh while the menu is open')
inventory.write_text(json.dumps(fixture))
for attempt in range(60):
    if run('return i._rows.length') == 9:
        break
    time.sleep(.25)
else:
    raise RuntimeError('Menu did not restore the inventory')
check(True, 'Second live refresh while the menu is open')
# Regression: a charging device without a reading keeps its pin and is identified
# in the panel by the device kind icon instead of an explained percentage.
check(run('return i._rows.find(r=>r.device.id==="charging-no-reading")._pin.visible'), 'Pin without battery reading')
check(run('return i._rows.find(r=>r.device.id==="charging-no-reading")._pin.reactive'), 'Pin without reading is reactive')
run('i._refresh();return true')
time.sleep(.3)
check(run('return i._rows.find(r=>r.device.id==="charging-no-reading")._pin.visible'), 'Pin survives a refresh')
check(run('return i._rows.find(r=>r.device.id==="light")._pin.visible') is False, 'No pin without battery support')
run('i._settings.set_boolean("show-percentage",true);i._selected="charging-no-reading";i._updatePanel();return true')
check(run('return i._deviceIcon.visible && i._percentage.visible===false'), 'Kind icon without percentage')
check(run('return i._deviceIcon.icon_name==="input-mouse-symbolic"'), 'Pinned kind icon is the mouse')
check(run('return i._button.accessible_name.includes("Synthetic charging mouse")'), 'Pinned name announced')
shot = str(Path(os.environ['SANDBOX'], 'pinned-kind-icon.png'))
subprocess.run(['gdbus', 'call', '--session', '--dest', 'org.gnome.Shell.Screenshot',
                '--object-path', '/org/gnome/Shell/Screenshot', '--method',
                'org.gnome.Shell.Screenshot.Screenshot', 'false', 'false', shot],
               text=True, capture_output=True, timeout=5)
print('Screenshot:', shot)
run('i._settings.set_boolean("show-percentage",true);i._selected="synthetic-a";i._updatePanel();return true')
check(run('return i._percentage.text') == '0%', 'Panel valid zero')
check(run('return i._deviceIcon.icon_name==="input-keyboard-symbolic"'), 'Pinned kind icon follows the device')
shot = str(Path(os.environ['SANDBOX'], 'pinned-percentage.png'))
subprocess.run(['gdbus', 'call', '--session', '--dest', 'org.gnome.Shell.Screenshot',
                '--object-path', '/org/gnome/Shell/Screenshot', '--method',
                'org.gnome.Shell.Screenshot.Screenshot', 'false', 'false', shot],
               text=True, capture_output=True, timeout=5)
print('Screenshot:', shot)
check(run('return i._timer>0 && i._delay===5'), 'Menu poll survives the preference change')
run('i._button.menu.close();return true')
time.sleep(.4)
check(run('return i._timer>0 && i._delay===60'), 'Closing the menu keeps the slow panel poll')
run('i._button.menu.open();return true')
time.sleep(.4)
check(run('return i._timer>0 && i._delay===5'), 'Reopening the menu restores the fast poll')
run('i._selected="duplicate";i._updatePanel();return true')
check(run('return i._percentage.visible') is False, 'Ambiguous ID not shown')
run('i._selected="offline";i._updatePanel();return true')
check(run('return i._percentage.visible') is False, 'Offline not shown')
run('i._selected="synthetic-b";i._updatePanel();return true')
check(run('return i._percentage.text') == '100%', 'Panel full')
# Preserve actors and focus across an unchanged refresh.
run('i._testRow=i._rows[0];i._refresh();return true')
time.sleep(.3)
check(run('return i._rows[0]===i._testRow'), 'Rows reused on refresh')
run('delete i._testRow;i._selected="synthetic-b";i._snapshot={inventory:"ready",devices:[]};i._render([]);i._updatePanel();return true')
check(run('return i._selected===null && !i._percentage.visible'), 'Disappearance resets selection')
# Real failure from fake CLI, not a mocked provider return.
fake = Path(os.environ['SANDBOX'], 'bin/fake-cli.py')
text = fake.read_text()
fake.write_text(text.replace("mode = sys.argv[1] if len(sys.argv) > 1 else 'valid'", "mode = 'agent_unavailable'"))
run('i._refresh();return true')
time.sleep(.3)
check(run('return i._rows.length===0 && !i._percentage.visible && i._snapshot===null'), 'Failure clears current data')
check(run('return i._status.label.text.includes("agent")'), 'Agent failure distinguished')
fake.write_text(text)
run('i._button.menu.close();i._button.menu.open();i._button.menu.close();i._button.menu.open();return true')
time.sleep(.3)
check(run('return i._rows.length') == 9, 'Rapid reopen recovers')
# A delayed real subprocess is cancelled while actors are destroyed.
fake.write_text(text.replace("mode = sys.argv[1] if len(sys.argv) > 1 else 'valid'", "mode = 'slow'"))
run('i._refresh();global.openlogiTestOld=i;extension.disable();return true')
time.sleep(.4)
check(evaluate('global.openlogiTestOld._pending===null && global.openlogiTestOld._timer===0 && global.openlogiTestOld._button===null'), 'Teardown releases ownership')
fake.write_text(text)
for cycle in range(3):
    evaluate('(()=>{const extension=' + prefix + ';extension.enable();return true})()')
    time.sleep(.25)
    check(run('return i._rows.length===9'), f'Reenable {cycle}')
    if cycle < 2:
        run('extension.disable();return true')
run('i._settings.set_boolean("show-percentage",false);return true')
check(run('return i._timer===0 && !i._percentage.visible'), 'Preference removes timer')
# Desktop activation against a private synthetic app with the installed desktop identity.
run('i._openApp();return true')
check(run('return i._status.label.text.includes("not installed")'), 'Missing desktop app')
desktop = Path(os.environ['SANDBOX'], 'data/applications/openlogi.desktop')
desktop.write_text('[Desktop Entry]\nType=Application\nName=Synthetic OpenLogi\nExec=/usr/bin/python3 ' + os.environ['SOURCE'] + '/tests/fake-gui.py\nStartupWMClass=org.openlogi.openlogi\nTerminal=false\n')
for attempt in range(60):
    if evaluate("!!Shell.AppSystem.get_default().lookup_app('openlogi.desktop')"):
        break
    time.sleep(.1)
else:
    raise RuntimeError('Synthetic launcher not detected')
run('i._openApp();return true')
windows = "global.get_window_actors().filter(a=>a.meta_window.get_wm_class()==='org.openlogi.openlogi')"
for attempt in range(60):
    if evaluate(windows + '.length') == 1:
        break
    time.sleep(.1)
else:
    raise RuntimeError('Synthetic GUI did not open')
check(True, 'Cold desktop activation (synthetic GUI)')
run('i._openApp();return true')
time.sleep(.3)
check(evaluate(windows + '.length') == 1, 'Warm activation creates no duplicate window (synthetic GUI)')
evaluate('(()=>{for(const a of ' + windows + ') a.meta_window.minimize();return true})()')
time.sleep(.2)
check(evaluate(windows + '.every(a=>a.meta_window.minimized)'), 'Synthetic GUI minimized')
run('i._openApp();return true')
time.sleep(.3)
check(evaluate(windows + '.every(a=>!a.meta_window.minimized)'), 'Minimized GUI activated (synthetic GUI)')
evaluate('(()=>{for(const a of ' + windows + ') a.meta_window.delete(global.get_current_time());return true})()')
# Long list, theme variants and font scaling run only in the isolated settings tree.
inventory_path = Path(os.environ['SANDBOX'], 'bin/inventory.json')
fixture = json.loads(inventory_path.read_text())
long_fixture = json.loads(json.dumps(fixture))
long_fixture['data']['devices'] = [dict(fixture['data']['devices'][0], id=f'synthetic-{n}', name=f'Synthetic {n:03d} ' + 'Long name ' * 20) for n in range(200)]
inventory_path.write_text(json.dumps(long_fixture))
run('i._refresh();return true')
time.sleep(.4)
check(run('return i._rows.length') == 200, 'Long inventory')
for theme in ['prefer-light', 'prefer-dark']:
    subprocess.run(['gsettings', 'set', 'org.gnome.desktop.interface', 'color-scheme', theme], check=True)
    for scale in [1.0, 1.5]:
        subprocess.run(['gsettings', 'set', 'org.gnome.desktop.interface', 'text-scaling-factor', str(scale)], check=True)
        run('i._button.menu.close();i._button.menu.open();return true')
        time.sleep(.3)
        check(run('return i._button.menu.actor.width <= Main.layoutManager.primaryMonitor.width'), f'Menu fits {theme} {scale}')
        check(run('return i._scroll.height < Main.layoutManager.primaryMonitor.height'), f'List scrolls {theme} {scale}')
        run('i._rows[0].grab_key_focus();return true')
        check(run('return global.stage.get_key_focus()===i._rows[0]'), f'Keyboard focus {theme} {scale}')
        shot = str(Path(os.environ['SANDBOX'], f'{theme}-{scale}.png'))
        result = subprocess.run(['gdbus', 'call', '--session', '--dest', 'org.gnome.Shell.Screenshot',
                                 '--object-path', '/org/gnome/Shell/Screenshot', '--method',
                                 'org.gnome.Shell.Screenshot.Screenshot', 'false', 'false', shot],
                                text=True, capture_output=True, timeout=5)
        print('Screenshot:', result.stdout.strip() or result.stderr.strip())
inventory_path.write_text(json.dumps(fixture))
run('i._button.menu.close();return true')
# Open the real GTK preferences process on this private bus and compositor.
subprocess.run(['gnome-extensions', 'prefs', 'openlogi-companion@giaffa86'], check=True, timeout=10)
for attempt in range(30):
    if evaluate("global.get_window_actors().some(a=>a.meta_window.get_wm_class()==='org.gnome.Shell.Extensions')"):
        break
    time.sleep(.1)
else:
    raise RuntimeError('Preferences window did not appear')
check(True, 'Preferences process opened')
evaluate("(()=>{for(const a of global.get_window_actors()) if(a.meta_window.get_wm_class()==='org.gnome.Shell.Extensions') a.meta_window.delete(global.get_current_time());return true})()")
time.sleep(.3)
check(evaluate("!global.get_window_actors().some(a=>a.meta_window.get_wm_class()==='org.gnome.Shell.Extensions')"), 'Preferences closed')
evaluate('delete global.openlogiTestOld')
print(f'{checks} isolated GNOME Shell checks passed; synthetic backend')
