def track_peer_performance(plugin):
    incomes = plugin.rpc.call("lightning-bkpr-listincome", {"consolidate_fees": True})
    peer_performance = []

    for income in incomes:
        peer_id = income['peer_id']
        earnings = income['earnings']
        forwards = income['forwarding_events']
        peer_performance.append((peer_id, earnings, forwards))

    # Sort by earnings
    peer_performance.sort(key=lambda x: x[1], reverse=True)

    top_5_peers = peer_performance[:5]
    bottom_5_peers = peer_performance[-5:]

    return top_5_peers, bottom_5_peers

