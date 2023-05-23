def get_peer_performance(plugin):
    """
    Fetches and returns the performance data for each peer.
    """
    try:
        incomes = plugin.rpc.call("lightning-bkpr-listincome", {"consolidate_fees": True})
    except Exception as e:
        # Log or handle the exception here
        return []

    peer_performance = []
    for income in incomes:
        peer_id = income['peer_id']
        earnings = income['earnings']
        forwards = income['forwarding_events']
        peer_performance.append((peer_id, earnings, forwards))

    return peer_performance

def get_top_and_bottom_peers(peer_performance):
    """
    Returns the top 5 and bottom 5 peers based on their earnings.
    """
    # Sort by earnings
    peer_performance.sort(key=lambda x: x[1], reverse=True)

    # Get the top 5 and bottom 5 peers
    top_5_peers = peer_performance[:5]
    bottom_5_peers = peer_performance[-5:]

    return top_5_peers, bottom_5_peers

def track_peer_performance(plugin):
    """
    Tracks and returns the performance of the top and bottom 5 peers.
    """
    peer_performance = get_peer_performance(plugin)
    top_5_peers, bottom_5_peers = get_top_and_bottom_peers(peer_performance)

    return top_5_peers, bottom_5_peers
