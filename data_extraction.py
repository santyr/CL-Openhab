def extract_channel_counts(channels):
    active_channels = len([c for c in channels if c['state'] == 'CHANNELD_NORMAL'])
    inactive_channels = len([c for c in channels if c['state'] != 'CHANNELD_NORMAL'])
    pending_channels = len([c for c in channels if c['state'] == 'CHANNELD_AWAITING_LOCKIN'])
    print('active_channels', active_channels)
    print('inactive_channels', inactive_channels)
    print('pending_channels', pending_channels)
    return active_channels, inactive_channels, pending_channels

def increment_transaction_counts(transaction_counts, plugin):
    transactions = plugin.rpc.listtransactions()
    incoming_transactions = [t for t in transactions if t['tx_type'] == 'incoming']
    outgoing_transactions = [t for t in transactions if t['tx_type'] == 'outgoing']
    transaction_counts['incoming_transaction_count'] += len(incoming_transactions)
    transaction_counts['outgoing_transaction_count'] += len(outgoing_transactions)
    return transaction_counts

def extract_data(plugin, transaction_counts):
    info = plugin.rpc.getinfo()
    node_id = info['id']
    alias = info['alias']
    blockheight = info['blockheight']
    network = info['network']
    version = info['version']
    channels = plugin.rpc.listchannels(source=info['id'])
    inactive_channels = plugin.rpc.listchannels_inactive(source=info['id'])
    pending_channels = plugin.rpc.listchannels_pending()
    peers = plugin.rpc.listpeers()

    # Calculate sum balance for each channel type
    active_channels_balance = sum([chan['satoshis'] for chan in active_channels['channels']])
    inactive_channels_balance = sum([chan['satoshis'] for chan in inactive_channels['channels']])
    pending_channels_balance = sum([chan['satoshis'] for chan in pending_channels['channels']])
    
    data = {
        'node_id': info['id'],
        'alias': info['alias'],
        'blockheight': info['blockheight'],
        'network': info['network'],
        'c_lightning_version': info['version'],
        'active_channels': active_channels,
        'inactive_channels': inactive_channels,
        'peers': len(peers),
        'incoming_transaction_count': transaction_counts['incoming_transaction_count'],
        'outgoing_transaction_count': transaction_counts['outgoing_transaction_count'],
        'cumulative_incoming_transaction_amount_sats': sum([t['amount_msat'] for t in transactions if t['tx_type'] == 'incoming']) // 1000,
        'cumulative_outgoing_transaction_amount_sats': sum([t['amount_msat'] for t in transactions if t['tx_type'] == 'outgoing']) // 1000,
        'pending_channels': pending_channels
    }

    return data

