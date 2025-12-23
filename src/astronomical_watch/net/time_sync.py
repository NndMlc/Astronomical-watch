"""
NTP time synchronization for precise astronomical time tracking.

Provides optional network time synchronization to ensure maximum accuracy
when system time might be slightly off.
"""
from __future__ import annotations
import socket
import struct
import time
from datetime import datetime, timezone, timedelta
from typing import Optional, Tuple
import threading

# NTP server configuration
DEFAULT_NTP_SERVER = "pool.ntp.org"
NTP_PORT = 123
NTP_TIMEOUT = 5.0  # seconds

# NTP packet format constants
NTP_PACKET_FORMAT = "!12I"
NTP_DELTA = 2208988800  # Seconds between 1900 and 1970

# Cache for synchronized time
_time_offset: Optional[float] = None
_last_sync: Optional[datetime] = None
_sync_lock = threading.Lock()


class TimeSyncError(Exception):
    """Raised when NTP synchronization fails."""
    pass


def _create_ntp_packet() -> bytes:
    """Create an NTP request packet."""
    # LI = 0, VN = 3, Mode = 3 (client)
    msg = b'\x1b' + 47 * b'\0'
    return msg


def _parse_ntp_response(data: bytes) -> float:
    """
    Parse NTP response and extract server time.
    
    Args:
        data: Raw NTP response packet
    
    Returns:
        Unix timestamp from NTP server
    
    Raises:
        TimeSyncError: If packet is invalid
    """
    if len(data) < 48:
        raise TimeSyncError(f"Invalid NTP packet size: {len(data)}")
    
    # Unpack the packet
    unpacked = struct.unpack(NTP_PACKET_FORMAT, data[0:48])
    
    # Extract transmit timestamp (when server sent reply)
    # This is in fields 10 and 11 (seconds and fraction)
    tx_timestamp = unpacked[10] + float(unpacked[11]) / 2**32
    
    # Convert from NTP epoch (1900) to Unix epoch (1970)
    unix_timestamp = tx_timestamp - NTP_DELTA
    
    return unix_timestamp


def sync_time_ntp(server: str = DEFAULT_NTP_SERVER, timeout: float = NTP_TIMEOUT) -> Tuple[float, float]:
    """
    Synchronize time with NTP server and calculate offset.
    
    Args:
        server: NTP server hostname
        timeout: Connection timeout in seconds
    
    Returns:
        Tuple of (ntp_timestamp, offset_seconds)
        - ntp_timestamp: Current time according to NTP server (Unix timestamp)
        - offset_seconds: Difference between NTP time and system time (positive means system is behind)
    
    Raises:
        TimeSyncError: If synchronization fails
    """
    try:
        # Record time before request
        t1 = time.time()
        
        # Create socket and send request
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(timeout)
            
            # Send NTP request
            packet = _create_ntp_packet()
            sock.sendto(packet, (server, NTP_PORT))
            
            # Receive response
            data, address = sock.recvfrom(1024)
        
        # Record time after response
        t4 = time.time()
        
        # Parse NTP response
        ntp_time = _parse_ntp_response(data)
        
        # Calculate round-trip time and offset
        # Simple approximation: assume symmetric delay
        round_trip = t4 - t1
        ntp_time_at_receive = ntp_time + round_trip / 2
        
        # Calculate offset (positive = system is behind NTP)
        offset = ntp_time_at_receive - t4
        
        return ntp_time, offset
        
    except socket.timeout:
        raise TimeSyncError(f"NTP request to {server} timed out after {timeout}s")
    except socket.gaierror as e:
        raise TimeSyncError(f"Could not resolve NTP server {server}: {e}")
    except socket.error as e:
        raise TimeSyncError(f"Network error contacting {server}: {e}")
    except Exception as e:
        raise TimeSyncError(f"Unexpected error during NTP sync: {e}")


def get_synchronized_time() -> datetime:
    """
    Get current UTC time, optionally adjusted by NTP offset.
    
    If time has been synchronized via sync_time_ntp(), returns system time
    adjusted by the calculated offset. Otherwise returns raw system time.
    
    Returns:
        Current UTC datetime, potentially adjusted for clock offset
    """
    with _sync_lock:
        if _time_offset is None:
            # No sync available, use system time
            return datetime.now(timezone.utc)
        
        # Apply offset to system time
        system_time = time.time()
        adjusted_time = system_time + _time_offset
        return datetime.fromtimestamp(adjusted_time, tz=timezone.utc)


def update_time_sync(server: str = DEFAULT_NTP_SERVER, force: bool = False) -> bool:
    """
    Update time synchronization with NTP server.
    
    Args:
        server: NTP server to use
        force: Force sync even if recently synchronized
    
    Returns:
        True if sync was successful, False otherwise
    """
    global _time_offset, _last_sync
    
    with _sync_lock:
        # Check if we need to sync
        if not force and _last_sync is not None:
            time_since_sync = datetime.now(timezone.utc) - _last_sync
            if time_since_sync < timedelta(minutes=10):
                # Recently synced, skip
                return True
        
        try:
            # Perform sync
            ntp_time, offset = sync_time_ntp(server)
            
            # Update cache
            _time_offset = offset
            _last_sync = datetime.now(timezone.utc)
            
            print(f"✅ NTP sync successful: offset = {offset*1000:.1f}ms")
            return True
            
        except TimeSyncError as e:
            print(f"⚠️  NTP sync failed: {e}")
            return False


def get_sync_status() -> dict:
    """
    Get current time synchronization status.
    
    Returns:
        Dictionary with sync information:
        - synced: bool - whether time has been synchronized
        - offset_ms: float - current offset in milliseconds (if synced)
        - last_sync: datetime - when last sync occurred (if synced)
        - age_seconds: float - seconds since last sync (if synced)
    """
    with _sync_lock:
        if _time_offset is None or _last_sync is None:
            return {
                "synced": False,
                "offset_ms": None,
                "last_sync": None,
                "age_seconds": None
            }
        
        age = (datetime.now(timezone.utc) - _last_sync).total_seconds()
        
        return {
            "synced": True,
            "offset_ms": _time_offset * 1000,
            "last_sync": _last_sync,
            "age_seconds": age
        }


def start_periodic_sync(interval_minutes: int = 60, server: str = DEFAULT_NTP_SERVER):
    """
    Start background thread for periodic time synchronization.
    
    Args:
        interval_minutes: Sync interval in minutes
        server: NTP server to use
    """
    def sync_worker():
        while True:
            update_time_sync(server, force=False)
            time.sleep(interval_minutes * 60)
    
    thread = threading.Thread(target=sync_worker, daemon=True, name="NTP-Sync")
    thread.start()
    print(f"🕐 Started periodic NTP sync (interval: {interval_minutes} min)")


# Convenience function for getting time with optional NTP sync
def now_utc(use_ntp: bool = True) -> datetime:
    """
    Get current UTC time, optionally using NTP synchronization.
    
    Args:
        use_ntp: If True and NTP has been synced, use adjusted time
    
    Returns:
        Current UTC datetime
    """
    if use_ntp:
        return get_synchronized_time()
    else:
        return datetime.now(timezone.utc)
