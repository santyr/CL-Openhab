from pyln.client import Plugin
import os
import json
import data_extraction
import openhab_utils
import performance_tracker

plugin = Plugin()
transaction_counts = [0, 0]

@plugin.init()
def init(options, configuration, plugin):
    plugin.log("c-lightning OpenHAB plugin initialized")

    # Configure OpenHAB API
    openhab_url, openhab_api_key = openhab_utils.configure_openhab_api()
    if not openhab_url or not openhab_api_key:
        plugin.log("Error: OPENHAB_URL or OPENHAB_API_KEY not set")
        plugin.stop() # Add this line to stop the plugin
        return

    # Define OpenHAB items
    openhab_items = define_openhab_items()

    # Check and create items if needed
    openhab_utils.check_and_create_items(openhab_url, openhab_api_key, openhab_items)


def define_openhab_items():
    return {
        'NodeID': {'type': 'String', 'label': 'Node ID', 'category': 'Network', 'tags': ['Status']},
        'Alias': {'type': 'String', 'label': 'Node Alias', 'category': 'Network', 'tags': ['Status']},
        'Blockheight': {'type': 'Number', 'label': 'Block Height', 'category': 'Network', 'tags': ['Status']},
        'Network': {'type': 'String', 'label': 'Network Type', 'category': 'Network', 'tags': ['Status']},
        'CLightningVersion': {'type': 'String', 'label': 'c-lightning Version', 'category': 'Network', 'tags': ['Status']},
        'ActiveChannels': {'type': 'Number', 'label': 'Active Channels', 'category': 'Network', 'tags': ['Status']},
        'InactiveChannels': {'type': 'Number', 'label': 'Inactive Channels', 'category': 'Network', 'tags': ['Status']},
        'Peers': {'type': 'Number', 'label': 'Peers', 'category': 'Network', 'tags': ['Status']},
        'IncomingTransactionCount': {'type': 'Number', 'label': 'Incoming Transactions', 'category': 'Network', 'tags': ['Status']},
        'OutgoingTransactionCount': {'type': 'Number', 'label': 'Outgoing Transactions', 'category': 'Network', 'tags': ['Status']},
        'CumulativeIncomingTransactionAmountSats': {'type': 'Number', 'label': 'Total Incoming Transaction Amount (sats)', 'category': 'Network', 'tags': ['Status']},
        'CumulativeOutgoingTransactionAmountSats': {'type': 'Number', 'label': 'Total Outgoing Transaction Amount (sats)', 'category': 'Network', 'tags': ['Status']},
        'PendingChannels': {'type': 'Number', 'label': 'Pending Channels', 'category': 'Network', 'tags': ['Status']},
        'Top1Peer': {'type': 'String', 'label': 'Top 1 Peer', 'category': 'Network', 'tags': ['Status']},
        'Top2Peer': {'type': 'String', 'label': 'Top 2 Peer', 'category': 'Network', 'tags': ['Status']},
        'Top3Peer': {'type': 'String', 'label': 'Top 1 Peer', 'category': 'Network', 'tags': ['Status']},
        'Top5Peer': {'type': 'String', 'label': 'Top 2 Peer', 'category': 'Network', 'tags': ['Status']},
        'Top5Peer': {'type': 'String', 'label': 'Top 1 Peer', 'category': 'Network', 'tags': ['Status']},
        'Bottom1Peer': {'type': 'String', 'label': 'Bottom 4 Peer', 'category': 'Network', 'tags': ['Status']},
        'Bottom2Peer': {'type': 'String', 'label': 'Bottom 4 Peer', 'category': 'Network', 'tags': ['Status']},
        'Bottom3Peer': {'type': 'String', 'label': 'Bottom 4 Peer', 'category': 'Network', 'tags': ['Status']},
        'Bottom4Peer': {'type': 'String', 'label': 'Bottom 4 Peer', 'category': 'Network', 'tags': ['Status']},
        'Bottom5Peer': {'type': 'String', 'label': 'Bottom 5 Peer', 'category': 'Network', 'tags': ['Status']},
    }

@plugin.subscribe("connect")
def on_connect(plugin, id, **kwargs):
    # Extract data from c-lightning
    data = data_extraction.extract_data(plugin, transaction_counts)

    # Track peer performance
    top_5_peers, bottom_5_peers = performance_tracker.track_peer_performance(plugin)
    for i, (peer_id, earnings, forwards) in enumerate(top_5_peers):
        data[f'Top{i + 1}Peer'] = f'ID: {peer_id}, Earnings: {earnings}, Forwards: {forwards}'
    for i, (peer_id, earnings, forwards) in enumerate(bottom_5_peers):
        data[f'Bottom{i + 1}Peer'] = f'ID: {peer_id}, Earnings: {earnings}, Forwards: {forwards}'

    # Send data to OpenHAB
    openhab_utils.send_data_to_openhab(openhab_url, openhab_api_key, data)

