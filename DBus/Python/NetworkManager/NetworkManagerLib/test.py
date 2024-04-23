from contextlib import suppress
import NetworkManager

class WifiManager:
  def __init__(self, interface_name):
    interface_name = ""

    self.wifi_dev = NetworkManager.NetworkManager.GetDeviceByIpIface(interface_name)
    self.wifi_dev.OnAccessPointAdded(self._ap_added)
    self.wifi_dev.OnAccessPointRemoved(self._ap_removed)
    self.wifi_dev.OnStateChanged(self._ap_state_changed)

    for ap in self.wifi_dev.GetAccessPoints():
      print(ap)
  
  def _ap_added(self, nm, interface, signal, access_point):
      with suppress(NetworkManager.ObjectVanished):
          access_point.OnPropertiesChanged(self._ap_prop_changed)
          print(access_point)
          #ssid = self._add_ap(access_point)
          #for cb in self._callbacks['scan_results']:
          #    args = (cb, [ssid], [])
          #    #GLib.idle_add(*args)

  def _ap_removed(self, dev, interface, signal, access_point):
      path = access_point.object_path
      if path in self.ssid_by_path:
          ssid = self.ssid_by_path[path]
          print(ssid)
          #self._remove_ap(path)
          #for cb in self._callbacks['scan_results']:
          #    args = (cb, [ssid], [])
          #    #GLib.idle_add(*args)

  def _ap_state_changed(self, nm, interface, signal, old_state, new_state, reason):
      msg = ""
      if new_state in (NetworkManager.NM_DEVICE_STATE_UNKNOWN, NetworkManager.NM_DEVICE_STATE_REASON_UNKNOWN):
          msg = "State is unknown"
      elif new_state == NetworkManager.NM_DEVICE_STATE_UNMANAGED:
          msg = "Error: Not managed by NetworkManager"
      elif new_state == NetworkManager.NM_DEVICE_STATE_UNAVAILABLE:
          msg = "Error: Not available for use:\nReasons may include the wireless switched off, missing firmware, etc."
      elif new_state == NetworkManager.NM_DEVICE_STATE_DISCONNECTED:
          msg = "Currently disconnected"
      elif new_state == NetworkManager.NM_DEVICE_STATE_PREPARE:
          msg = "Preparing the connection to the network"
      elif new_state == NetworkManager.NM_DEVICE_STATE_CONFIG:
          msg = "Connecting to the requested network..."
      elif new_state == NetworkManager.NM_DEVICE_STATE_NEED_AUTH:
          msg = "Authorizing"
      elif new_state == NetworkManager.NM_DEVICE_STATE_IP_CONFIG:
          msg = "Requesting IP addresses and routing information"
      elif new_state == NetworkManager.NM_DEVICE_STATE_IP_CHECK:
          msg = "Checking whether further action is required for the requested network connection"
      elif new_state == NetworkManager.NM_DEVICE_STATE_SECONDARIES:
          msg = "Waiting for a secondary connection (like a VPN)"
      elif new_state == NetworkManager.NM_DEVICE_STATE_ACTIVATED:
          msg = "Connected"
      elif new_state == NetworkManager.NM_DEVICE_STATE_DEACTIVATING:
          msg = "A disconnection from the current network connection was requested"
      elif new_state == NetworkManager.NM_DEVICE_STATE_FAILED:
          msg = "Failed to connect to the requested network"
          self.callback("popup", msg)
      elif new_state == NetworkManager.NM_DEVICE_STATE_REASON_DEPENDENCY_FAILED:
          msg = "A dependency of the connection failed"
      elif new_state == NetworkManager.NM_DEVICE_STATE_REASON_CARRIER:
          msg = ""
      else:
          print(f"State {new_state}")
      if msg != "":
          print("Connecting status:", msg)

      if new_state == NetworkManager.NM_DEVICE_STATE_ACTIVATED:
          self.connected = True
          for cb in self._callbacks['connected']:
              args = (cb, self.get_connected_ssid(), None)
      else:
          self.connected = False

print("START ...")
wifi_manager = WifiManager("wlan0")
print("END ...")
