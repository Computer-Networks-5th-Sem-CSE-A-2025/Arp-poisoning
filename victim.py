from scapy.all import Ether, ARP, srp, sniff, conf
import time
import platform
import subprocess
def turn_on_wifi():
    system_platform = platform.system()
    if system_platform == "Windows":
        subprocess.run(["netsh", "interface", "set", "interface", "Wi-Fi", "enable"], capture_output=True, text=True)
    elif system_platform == "Darwin":  # macOS
        subprocess.run(["networksetup", "-setairportpower", "en0", "on"], capture_output=True, text=True)
    elif system_platform == "Linux":
        # You may need to replace "wlp2s0" with your actual wireless interface name on Linux
        subprocess.run(["sudo", "ip", "link", "set", "dev", "wlp2s0", "up"], capture_output=True, text=True)
    else:
        print("Unsupported operating system")
        
def turn_off_wifi():
    system_platform = platform.system()
    if system_platform == "Windows":
        subprocess.run(["netsh", "interface", "set", "interface", "Wi-Fi", "disable"], capture_output=True, text=True)
    elif system_platform == "Darwin":  # macOS
        subprocess.run(["networksetup", "-setairportpower", "en0", "off"], capture_output=True, text=True)
    elif system_platform == "Linux":
        # You may need to replace "wlp2s0" with your actual wireless interface name on Linux
        subprocess.run(["sudo", "ip", "link", "set", "dev", "wlp2s0", "down"], capture_output=True, text=True)
    else:
        print("Unsupported operating system")
    try:
        while(True):
            continue
    except KeyboardInterrupt:
        turn_on_wifi()

def get_mac(ip):
    """
    Returns the MAC address of `ip`, if it is unable to find it
    for some reason, throws `IndexError`
    """
    p = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip)
    result = srp(p, timeout=3, verbose=False)[0]
    return result[0][1].hwsrc

def process(packet):
    # if the packet is an ARP packet
    if packet.haslayer(ARP):
        # if it is an ARP response (ARP reply)
        if packet[ARP].op == 2:
            try:
                # get the real MAC address of the sender
                real_mac = get_mac(packet[ARP].psrc)
                # get the MAC address from the packet sent to us
                response_mac = packet[ARP].hwsrc
                # if they're different, definitely there is an attack
                if real_mac != response_mac:
                    print(f"[!] You are under attack, REAL-MAC: {real_mac.upper()}, FAKE-MAC: {response_mac.upper()}")
                    print("Turning off wifi in 3 sec")
                    time.sleep(3)
                    turn_off_wifi()
            except IndexError:
                # unable to find the real mac
                # may be a fake IP or firewall is blocking packets
                pass
sniff(store=False, prn=process)            
