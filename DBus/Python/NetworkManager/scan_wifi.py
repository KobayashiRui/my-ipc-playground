import dbus, sys

bus = dbus.SystemBus()
service_name = "org.freedesktop.NetworkManager"
proxy = bus.get_object(service_name, "/org/freedesktop/NetworkManager/Settings")
settings = dbus.Interface(proxy, "org.freedesktop.NetworkManager.Settings")

if len(sys.argv) != 2:
    print("Usage: %s <ifname>" % sys.argv[0])
    sys.exit(0)

#インターフェースの名前からobjectのpathを取得する
"""
dbus-send --system --print-reply \
    --dest=org.freedesktop.NetworkManager \
    /org/freedesktop/NetworkManager \
    org.freedesktop.NetworkManager.GetDeviceByIpIface \
    string:"wlan0"
"""
iface = sys.argv[1]
proxy = bus.get_object(service_name, "/org/freedesktop/NetworkManager")
nm = dbus.Interface(proxy, "org.freedesktop.NetworkManager")
devpath = nm.GetDeviceByIpIface(iface)
print(devpath)

# 取得したdevpathを使用してアクセスポイントのリストを取得する
device = bus.get_object("org.freedesktop.NetworkManager", devpath)
wireless_device = dbus.Interface(device, "org.freedesktop.NetworkManager.Device.Wireless")
access_points = wireless_device.GetAccessPoints()
for ap_path in access_points:
    ap = bus.get_object("org.freedesktop.NetworkManager", ap_path)
    ap_properties = dbus.Interface(ap, dbus.PROPERTIES_IFACE)
    ssid = ap_properties.Get("org.freedesktop.NetworkManager.AccessPoint", "Ssid")
    # SSIDはバイト列なので、文字列に変換
    ssid_str = ''.join(chr(b) for b in ssid)
    strength = ap_properties.Get("org.freedesktop.NetworkManager.AccessPoint", "Strength")
    strength_int = int(strength)
    print(f"SSID: {ssid_str}, Strength: {strength_int}%")

sys.exit(0)