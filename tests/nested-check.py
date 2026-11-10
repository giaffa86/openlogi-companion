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
    return evaluate('(()=>{const extension=' + prefix + ';const i=extension._indicator;const p=i._panelDevices.values().next().value;' + body + '})()')
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
check(run('return i._rows.every(r=>!r.reactive && !r.can_focus && !r.track_hover)'), 'Device rows have no click, focus or hover action')
check(run('return i._rows.every(r=>!r._clickGesture.enabled)'), 'Device row click gestures disabled')
check(run('return i._rows.every(r=>r.accessible_name.length>0)'), 'Accessible row names')
check(run('return i._rows.filter(r=>r._pin.visible).every(r=>r._pin.accessible_name.includes(r._name.text) && r._pin.accessible_name.includes(r._detail.text))'), 'Pins announce their device and battery without focusing the row')
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
run('i._settings.set_boolean("show-percentage",true);i._selected=new Set(["charging-no-reading"]);i._updatePanel();return true')
check(run('return Boolean(p) && (p?.label.visible ?? false)===false'), 'Kind icon without percentage')
check(run('return p.icon.icon_name==="input-mouse-symbolic"'), 'Pinned kind icon is the mouse')
check(run('return i._button.accessible_name.includes("Synthetic charging mouse")'), 'Pinned name announced')
shot = str(Path(os.environ['SANDBOX'], 'pinned-kind-icon.png'))
subprocess.run(['gdbus', 'call', '--session', '--dest', 'org.gnome.Shell.Screenshot',
                '--object-path', '/org/gnome/Shell/Screenshot', '--method',
                'org.gnome.Shell.Screenshot.Screenshot', 'false', 'false', shot],
               text=True, capture_output=True, timeout=5)
print('Screenshot:', shot)
run('i._settings.set_boolean("show-percentage",true);i._selected=new Set(["synthetic-a"]);i._updatePanel();return true')
check(run('return p.label.text') == '0%', 'Panel valid zero')
check(run('return p.icon.icon_name==="input-keyboard-symbolic"'), 'Pinned kind icon follows the device')
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
run('i._selected=new Set(["duplicate"]);i._updatePanel();return true')
check(run('return (p?.label.visible ?? false)') is False, 'Ambiguous ID not shown')
check(run('return i._logo.visible'), 'No pinned device keeps the extension logo')
run('i._selected=new Set(["offline"]);i._updatePanel();return true')
check(run('return (p?.label.visible ?? false)') is False, 'Offline not shown')
check(run('return i._logo.visible && !p'), 'Offline device never hides the logo')
run('i._selected=new Set(["synthetic-b"]);i._updatePanel();return true')
check(run('return p.label.text') == '100%', 'Panel full')
# The extension logo can be replaced by the pinned device icon and percentage.
run('i._settings.set_boolean("hide-logo",true);i._updatePanel();return true')
check(run('return !i._logo.visible && Boolean(p) && p.label.text==="100%"'), 'Pinned device hides the extension logo')
check(run('return i._button.accessible_name.includes("Synthetic keyboard")'), 'Hidden logo keeps the accessible name')
shot = str(Path(os.environ['SANDBOX'], 'pinned-no-logo.png'))
subprocess.run(['gdbus', 'call', '--session', '--dest', 'org.gnome.Shell.Screenshot',
                '--object-path', '/org/gnome/Shell/Screenshot', '--method',
                'org.gnome.Shell.Screenshot.Screenshot', 'false', 'false', shot],
               text=True, capture_output=True, timeout=5)
print('Screenshot:', shot)
run('i._settings.set_boolean("hide-logo",false);i._updatePanel();return true')
check(run('return i._logo.visible'), 'Disabling the preference restores the extension logo')
run('i._settings.set_boolean("hide-logo",true);i._updatePanel();return true')
check(run('return !i._logo.visible'), 'Preference change applies without a refresh')
# Use the actual pin buttons: each toggles independently and keeps insertion order.
run('i._selected.clear();i._render(i._snapshot.devices);i._updatePanel();return true')
for device_id in ['synthetic-a', 'synthetic-b', 'charging-no-reading']:
    run(f'i._rows.find(r=>r.device.id==="{device_id}")._pin.emit("clicked",0);return true')
check(run('return i._selected.size===3 && i._panelDevices.size===3'), 'Three pins coexist')
check(run('return i._rows.filter(r=>r._pin.has_style_pseudo_class("checked")).length===3'), 'All selected pins marked')
check(run('return [...i._panelDevices.values()].map(p=>p.label.text)') == ['0%', '100%', ''], 'Independent numeric readings')
run('i._rows.find(r=>r.device.id==="synthetic-a")._pin.emit("clicked",0);return true')
check(run('return [...i._selected]') == ['synthetic-b', 'charging-no-reading'], 'Unpin removes only that device')
run('i._rows.find(r=>r.device.id==="synthetic-a")._pin.emit("clicked",0);return true')
check(run('return [...i._panelDevices.keys()]') == ['synthetic-b', 'charging-no-reading', 'synthetic-a'], 'Re-pinned device follows others')
run('i._testPanel=i._panelDevices.get("synthetic-b");i._refresh();return true')
time.sleep(.3)
check(run('return i._selected.size===3 && i._panelDevices.get("synthetic-b")===i._testPanel'), 'Refresh preserves all pins and actors')
run('i._settings.set_boolean("show-percentage",false);return true')
check(run('return i._selected.size===3 && i._panelDevices.size===0 && i._logo.visible'), 'Hiding panel devices preserves session choices')
run('i._settings.set_boolean("show-percentage",true);return true')
check(run('return i._panelDevices.size===3'), 'Showing devices restores all pins')
run('delete i._testPanel;i._settings.set_boolean("battery-bar",true);return true')
check(run('return [...i._panelDevices.values()].every(p=>!p.label.visible)'), 'Bar switch hides numeric labels live')
check(run('return i._panelDevices.get("synthetic-a").bar.visible && !i._panelDevices.get("synthetic-a").fill.visible'), 'Zero has an empty bar')
check(run('return !i._panelDevices.get("charging-no-reading").bar.visible'), 'Missing reading never becomes an empty bar')
check(run('return i._panelDevices.get("synthetic-b").bar.visible && i._panelDevices.get("synthetic-b").fill.visible'), 'Full bar is visible')
time.sleep(.2)
check(run('return Math.abs(p.fill.height-p.bar.height)<1'), 'Full bar fills the track')
check(run('return i._button.accessible_name.includes("100%") && i._button.accessible_name.includes("Charging")'), 'Bars keep numeric and charging accessible details')
# Update a real synthetic CLI response, then inspect proportional fill and colours.
changed = json.loads(json.dumps(fixture))
next(d for d in changed['data']['devices'] if d['id'] == 'charging-no-reading')['battery']['percentage'] = 65
inventory.write_text(json.dumps(changed))
run('i._rows.find(r=>r.device.id==="synthetic-a")._pin.emit("clicked",0);i._refresh();return true')
time.sleep(.3)
check(run('const mouse=i._panelDevices.get("charging-no-reading");return Math.abs(mouse.fill.height/mouse.bar.height-.65)<.08'), 'Bar tracks reported percentage')
check(run('return i._panelDevices.get("charging-no-reading").fill.style_class==="openlogi-companion-battery-fill"'), 'Normal bar uses green')
run('i._button.menu.close();return true')
time.sleep(.2)
shot = str(Path(os.environ['SANDBOX'], 'multiple-pinned-bars.png'))
subprocess.run(['gdbus', 'call', '--session', '--dest', 'org.gnome.Shell.Screenshot',
                '--object-path', '/org/gnome/Shell/Screenshot', '--method',
                'org.gnome.Shell.Screenshot.Screenshot', 'false', 'false', shot],
               text=True, capture_output=True, timeout=5)
print('Screenshot:', shot)
run('i._rows.find(r=>r.device.id==="long")._pin.emit("clicked",0);return true')
check(run('return i._panelDevices.get("long").fill.has_style_class_name("low")'), 'Low bar uses amber')
run('i._rows.find(r=>r.device.id==="synthetic-a")._pin.emit("clicked",0);return true')
check(run('return i._panelDevices.get("synthetic-a").fill.has_style_class_name("critical")'), 'Critical bar uses red')
changed['data']['devices'] = [d for d in changed['data']['devices'] if d['id'] != 'synthetic-b']
inventory.write_text(json.dumps(changed))
run('i._refresh();return true')
time.sleep(.3)
check(run('return !i._selected.has("synthetic-b") && i._selected.size===3'), 'Disappearance removes only the missing pin')
inventory.write_text(json.dumps(fixture))
run('i._refresh();return true')
time.sleep(.3)
check(run('return !i._selected.has("synthetic-b") && i._selected.has("charging-no-reading")'), 'Reappearance does not auto-pin; missing reading preserves its pin')
changed = json.loads(json.dumps(fixture))
next(d for d in changed['data']['devices'] if d['id'] == 'synthetic-a')['online'] = False
inventory.write_text(json.dumps(changed))
run('i._refresh();return true')
time.sleep(.3)
check(run('return !i._selected.has("synthetic-a") && i._selected.size===2'), 'Disconnect removes only that pin')
changed['data']['devices'].append(next(d.copy() for d in changed['data']['devices'] if d['id'] == 'long'))
inventory.write_text(json.dumps(changed))
run('i._refresh();return true')
time.sleep(.3)
check(run('return !i._selected.has("long") && i._selected.size===1 && !i._logo.visible'), 'Ambiguity removes only that pin and keeps the visible device')
inventory.write_text(json.dumps(fixture))
run('i._refresh();return true')
time.sleep(.3)
run('i._rows.find(r=>r.device.id==="long")._pin.emit("clicked",0);return true')
run('i._settings.set_boolean("battery-bar",false);return true')
check(run('return i._panelDevices.get("long").label.text==="20%" && !i._panelDevices.get("long").bar.visible'), 'Switch restores numeric readings')
run('i._button.menu.open();return true')
# Preserve actors and focus across an unchanged refresh.
run('i._testRow=i._rows[0];i._refresh();return true')
time.sleep(.3)
check(run('return i._rows[0]===i._testRow'), 'Rows reused on refresh')
run('delete i._testRow;i._selected=new Set(["synthetic-b"]);i._snapshot={inventory:"ready",devices:[]};i._render([]);i._updatePanel();return true')
check(run('return i._selected.size===0 && i._panelDevices.size===0'), 'Disappearance resets all selections')
# Real failure from fake CLI, not a mocked provider return.
run('i._refresh();return true')
time.sleep(.3)
run('for(const id of ["synthetic-a","charging-no-reading"]) i._rows.find(r=>r.device.id===id)._pin.emit("clicked",0);return true')
check(run('return i._selected.size===2 && i._panelDevices.size===2'), 'Two active pins before cleanup')
fake = Path(os.environ['SANDBOX'], 'bin/fake-cli.py')
text = fake.read_text()
fake.write_text(text.replace("mode = sys.argv[1] if len(sys.argv) > 1 else 'valid'", "mode = 'agent_unavailable'"))
run('i._refresh();return true')
time.sleep(.3)
check(run('return i._rows.length===0 && i._panelDevices.size===0 && i._selected.size===0 && i._snapshot===null'), 'Failure clears all pins and current data')
check(run('return i._status.label.text.includes("agent")'), 'Agent failure distinguished')
fake.write_text(text)
run('i._button.menu.close();i._button.menu.open();i._button.menu.close();i._button.menu.open();return true')
time.sleep(.3)
check(run('return i._rows.length') == 9, 'Rapid reopen recovers')
# A delayed real subprocess is cancelled while actors are destroyed.
run('for(const id of ["synthetic-a","charging-no-reading"]) i._rows.find(r=>r.device.id===id)._pin.emit("clicked",0);return true')
check(run('return i._selected.size===2 && i._panelDevices.size===2'), 'Two active pins before cleanup')
fake.write_text(text.replace("mode = sys.argv[1] if len(sys.argv) > 1 else 'valid'", "mode = 'slow'"))
run('i._refresh();global.openlogiTestOld=i;extension.disable();return true')
time.sleep(.4)
check(evaluate('global.openlogiTestOld._pending===null && global.openlogiTestOld._timer===0 && global.openlogiTestOld._button===null && global.openlogiTestOld._panelDevices.size===0 && global.openlogiTestOld._selected.size===0'), 'Teardown releases ownership and all pins')
fake.write_text(text)
for cycle in range(3):
    evaluate('(()=>{const extension=' + prefix + ';extension.enable();return true})()')
    time.sleep(.25)
    check(run('return i._rows.length===9'), f'Reenable {cycle}')
    if cycle < 2:
        run('extension.disable();return true')
run('i._settings.set_boolean("show-percentage",false);return true')
check(run('return i._timer===0 && !p?.label.visible'), 'Preference removes timer')
check(run('return i._logo.visible'), 'Panel without the pinned device keeps the extension logo')
run('i._settings.set_boolean("hide-logo",false);return true')
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
run('i._settings.set_boolean("show-percentage",true);i._settings.set_boolean("battery-bar",true);'
    'i._rows[0]._pin.emit("clicked",0);i._rows[1]._pin.emit("clicked",0);return true')
for theme in ['prefer-light', 'prefer-dark']:
    subprocess.run(['gsettings', 'set', 'org.gnome.desktop.interface', 'color-scheme', theme], check=True)
    for scale in [1.0, 1.5]:
        subprocess.run(['gsettings', 'set', 'org.gnome.desktop.interface', 'text-scaling-factor', str(scale)], check=True)
        run('i._button.menu.close();i._button.menu.open();return true')
        time.sleep(.3)
        check(run('return i._button.menu.actor.width <= Main.layoutManager.primaryMonitor.width'), f'Menu fits {theme} {scale}')
        check(run('return i._scroll.height < Main.layoutManager.primaryMonitor.height'), f'List scrolls {theme} {scale}')
        run('i._rows[0]._pin.grab_key_focus();return true')
        check(run('return global.stage.get_key_focus()===i._rows[0]._pin'), f'Keyboard focus on pin {theme} {scale}')
        check(run('return i._panelDevices.size===2 && [...i._panelDevices.values()].every(p=>p.bar.width>0 && p.bar.height>0)'), f'Visible bars {theme} {scale}')
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
shot = str(Path(os.environ['SANDBOX'], 'preferences.png'))
time.sleep(.3)
subprocess.run(['gdbus', 'call', '--session', '--dest', 'org.gnome.Shell.Screenshot',
                '--object-path', '/org/gnome/Shell/Screenshot', '--method',
                'org.gnome.Shell.Screenshot.Screenshot', 'false', 'false', shot],
               text=True, capture_output=True, timeout=5)
print('Screenshot:', shot)
evaluate("(()=>{for(const a of global.get_window_actors()) if(a.meta_window.get_wm_class()==='org.gnome.Shell.Extensions') a.meta_window.delete(global.get_current_time());return true})()")
time.sleep(.3)
check(evaluate("!global.get_window_actors().some(a=>a.meta_window.get_wm_class()==='org.gnome.Shell.Extensions')"), 'Preferences closed')
evaluate('delete global.openlogiTestOld')
print(f'{checks} isolated GNOME Shell checks passed; synthetic backend')
