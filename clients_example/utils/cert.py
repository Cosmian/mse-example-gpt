import socket
import ssl
import tempfile
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse


def get_ssl_certificate(url: str) -> Optional[str]:
    """
    Retrieves the SSL certificate of a remote host.

    By default the app is deployed in zero trust mode with a SSL certificate generated by the enclave itself.
    For simplicity, here we just trust the provided cert, but in real world use, one would need to verify it.
    More information: https://docs.cosmian.com/microservice_encryption/how_it_works_use/
    """
    parsed_url = urlparse(url)

    cert_path: Optional[str] = None
    if parsed_url.scheme == "http":
        return None

    hostname, port = parsed_url.hostname, 443
    if not hostname:
        raise Exception(f"Not hostname found in url: {url}")

    cert_path = Path(tempfile.gettempdir()) / f"{hostname}.pem"

    with socket.create_connection((hostname, port)) as sock:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            bin_cert = ssock.getpeercert(True)
            if not bin_cert:
                raise Exception(f"Can't get peer certificate for url: {url}")
            cert_data = ssl.DER_cert_to_PEM_cert(bin_cert)

    cert_path.write_bytes(cert_data.encode("utf-8"))

    return str(cert_path)