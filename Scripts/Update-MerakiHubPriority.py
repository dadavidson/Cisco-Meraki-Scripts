#!/usr/bin/env python3

__author__ = "Daniel Davidson"
__version__ = "0.1.0"
__license__ = "MIT"

# Import modules
import argparse
import time
from datetime import datetime

# Custom modules
import meraki


def main():
    # Terminal colors
    class Colors:
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        PURPLE = '\033[95m'
        ENDC = '\033[0m'

    # Instantiate a Meraki dashboard API session
    # Import your API key
    API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    dashboard = meraki.DashboardAPI(
        API_KEY,
        print_console=False
        )

    # Get list of organizations
    # my_orgs = dashboard.organizations.getOrganizations()
    # print(my_orgs)
    # Import your ORG ID
    act_org_id = '123456'

    pr = argparse.ArgumentParser(description='Meraki API Hub Priority Tool')
    pr.add_argument('--hub', required=True,
                    help='Choose a Hub (DC1 or DC2)')
    args = pr.parse_args()

    # Get list of networks in organization
    try:
        networks = dashboard.organizations.getOrganizationNetworks(act_org_id)
    except meraki.APIError as e:
        print(f'Meraki API error: {e}')
        # print(f'status code = {e.status}')
        # print(f'reason = {e.reason}')
        print(f'error = {e.message}')
    except Exception as e:
        print(f'some other error: {e}')
    
    # print(*networks, sep='\n\n')
    print(f'{Colors.GREEN} [+] Choosing HUB: {args.hub} {Colors.ENDC}')

    # Targeted networks
    # Input each network id you would like to target
    # Below network id's are just examples
    netid_list = [
        'L_123456789012345678', 'L_123456789012345678',
        'L_123456789012345678', 'L_123456789012345678',
        'L_123456789012345678'
    ]
    target = len(netid_list)

    # Iterate through networks
    print(f'{Colors.BLUE} [~] Total networks: {len(networks)} {Colors.ENDC}')
    print(f'{Colors.BLUE} [~] Targeted networks: {target}\n')
    mode = 'spoke'
    counter = 0
    for net in netid_list:
        counter += 1
        networkId = net
        netobj = next(
            (item for item in networks if item["id"] == net), None
            )
        netname = next(
            (item['name'] for item in networks if item["id"] == net), None
            )
        print(f'{Colors.YELLOW} [{counter}/{target}] NETWORK: {netname}')
        # print(f'{Colors.BLUE} {netobj} {Colors.ENDC}')

        # Set Site to Site VPN Hub Priority
        if args.hub == 'HUB1':
            # MX250 HUB #1
            req = dashboard.appliance.updateNetworkApplianceVpnSiteToSiteVpn(
                networkId, mode,
                hubs=[
                    {'hubId': 'N_123456789012345678', 'useDefaultRoute': True}, # Set HUB 1 ID as primary hub
                    {'hubId': 'N_098765432109876543', 'useDefaultRoute': True}] # Set HUB 2 ID as secondary hub
            )
            print(f'{Colors.GREEN} [+] NET ID: {networkId} complete\n')
        elif args.hub == 'HUB2':
            # MX250 HUB #2
            req = dashboard.appliance.updateNetworkApplianceVpnSiteToSiteVpn(
                networkId, mode,
                hubs=[
                    {'hubId': 'N_098765432109876543', 'useDefaultRoute': True}, # Set HUB 2 ID as primary hub
                    {'hubId': 'N_123456789012345678', 'useDefaultRoute': True}] # Set HUB 1 ID as secondary hub
            )
            print(f'{Colors.GREEN} [+] NET ID: {networkId} complete\n')
        else:
            print('Not a valid hub')

    print(f'{Colors.ENDC}')


if __name__ == '__main__':
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    print(f'Script complete, total runtime {end_time - start_time}\n')
