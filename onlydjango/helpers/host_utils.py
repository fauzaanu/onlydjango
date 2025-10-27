def normalize_host(host_input):
    """Normalize host by removing protocol and www prefix"""
    if not host_input:
        return 'onlydjango.com'
    
    host = host_input.replace('https://', '').replace('http://', '')
    host = host.rstrip('/')
    
    if host.startswith('www.'):
        host = host[4:]
    
    return host