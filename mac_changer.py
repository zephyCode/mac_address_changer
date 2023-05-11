#!/usr/bin/env python3

import subprocess
import optparse
import re


def change_mac(interface, new_mac):
    subprocess.call(['ifconfig', interface, 'down'])
    print('Changing the MAC address for ' + interface + " to " + new_mac)
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['ifconfig', interface, 'up'])
    # print('--------------------------------------------------------------------------------------------------------------------------')
    # print('Output is below')
    # subprocess.call(['ifconfig', interface])
    # print('--------------------------------------------------------------------------------------------------------------------------')


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest='interface', help="Interface of which the MAC address is to be changed. For eg: eth0, wlan0 etc.")
    parser.add_option('-m', '--mac', dest='new_mac', help="New MAC address. Format eg (00:aa:bb:11:cc:dd)")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error('[-] Please specify an interface, use --help for more info.')
    elif not options.new_mac:
        parser.error('[-] Please specify a new mac, use --help for more info.')
    return options


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(['ifconfig', interface]).decode()
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")


options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Current MAC = "+str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print('[+] MAC address was successfully changed to '+current_mac)
else:
    print('[-] MAC address did not changed.')


