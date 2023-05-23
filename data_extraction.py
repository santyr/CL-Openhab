def extract_channel_counts(channels):
    active_channels = len([c for c in channels if c['state'] == 'CHANNELD_NORMAL'])
    inactive_channels = len([c for c in channels if c['state'] != 'CHANNELD_NORMAL'])
    pending_channels = len([c for c in channels if c['state'] == 'CHANNELD_AWAITING_LOCKIN'])
    return active_channels, inactive_channels, pending_channels

def increment_transaction_counts(transaction_counts, plugin):
    try:
        transactions = plugin.rpc.listtransactions()
    except Exception as e:
        # handle or log the exception
        return transaction_counts

    incoming_transactions = [t for t in transactions if t['tx_type'] == 'incoming']
    outgoing_transactions = [t for t in transactions if t['tx_type'] == 'outgoing']
    transaction_counts['incoming_transaction_count'] += len(incoming_transactions)
    transaction_counts['outgoing_transaction_count'] += len(outgoing_transactions)
    return transaction_counts

def get_node_info(plugin):
    try:
        info = plugin.rpc.getinfo()
    except Exception as e:
        # handle or log the exception
        return None

    node_id = info['id']
    alias = info['alias']
    blockheight = info['blockheight']
    network = info['network']
    version = info['version']

    return node_id, alias, blockheight, network, version

def get_channels(plugin, node_id):
    try:
        active_channels = plugin.rpc.listchannels(source=node_id)
        inactive_channels = plugin.rpc.listchannels_inactive(source=node_id)
        pending_channels = plugin.rpc.listchannels_pending()
    except Exception as e:
        # handle or log the exception
        return None, None, None

    return active_channels, inactive_channels, pending_channels

def get_peers(plugin):
    try:
        peers = plugin.rpc.listpeers()
    except Exception as e:
        # handle or log the exception
        return None

    return peers

def extract_data(plugin, transaction_counts):
    node_id, alias, blockheight, network, version = get_node_info(plugin)
    active_channels, inactive_channels, pending_channels = get_channels(plugin, node_id)
    peers = get_peers(plugin)

    if None in [node_id, active_channels, peers]:
        # handle missing data
        return None

    data = {
        'node_id': node_id,
        'alias': alias,
        'blockheight': blockheight'network': network,
        'c_lightning_version': version,
        'active_channels': len(active_channels['channels']),
        'inactive_channels': len(inactive_channels['channels']),
        'peers': len(peers),
        'incoming_transaction_count': transaction_counts['incoming_transaction_count'],
        'outgoing_transaction_count': transaction_counts['outgoing_transaction_count'],
        'cumulative_incoming_transaction_amount_sats': sum([t['amount_msat'] for t in transactions if t['tx_type'] == 'incoming']) // 1000,
        'cumulative_outgoing_transaction_amount_sats': sum([t['amount_msat'] for t in transactions if t['tx_type'] == 'outgoing']) // 1000,
        'pending_channels': len(pending_channels['channels']),
    }

    return data


