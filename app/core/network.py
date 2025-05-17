import socket
import requests
import logging

logger = logging.getLogger(__name__)

def check_connectivity():
    """Verifica la conectividad a servicios externos"""
    services = {
        'Firebase': 'https://firebase.google.com',
        'Supabase': 'https://supabase.co',
        'Google': 'https://www.google.com'
    }
    
    # Verificar resolución DNS
    try:
        socket.getaddrinfo('firebase.google.com', 443)
        socket.getaddrinfo('supabase.co', 443)
        logger.info("✅ DNS resolution working")
    except socket.gaierror as e:
        logger.error(f"❌ DNS resolution failed: {e}")
        return False

    # Verificar conectividad HTTP
    for service, url in services.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                logger.info(f"✅ Connection to {service} successful")
            else:
                logger.warning(f"⚠️ Connection to {service} returned status {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to connect to {service}: {e}")
            return False
    
    return True 