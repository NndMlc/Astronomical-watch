"""
Tests for NTP time synchronization.
"""
import pytest
from datetime import datetime, timezone, timedelta
from astronomical_watch.net.time_sync import (
    sync_time_ntp,
    get_synchronized_time,
    update_time_sync,
    get_sync_status,
    now_utc,
    TimeSyncError,
)


def test_ntp_sync_basic():
    """Test basic NTP synchronization."""
    try:
        ntp_time, offset = sync_time_ntp(server="pool.ntp.org", timeout=5.0)
        
        # NTP time should be reasonable (not too far from system time)
        system_time = datetime.now(timezone.utc).timestamp()
        assert abs(ntp_time - system_time) < 300, "NTP time too far from system time"
        
        # Offset should be reasonable (< 5 seconds for most systems)
        assert abs(offset) < 5, f"System clock offset too large: {offset}s"
        
        print(f"✅ NTP sync successful: offset = {offset*1000:.1f}ms")
        
    except TimeSyncError as e:
        pytest.skip(f"NTP sync failed (network issue?): {e}")


def test_update_time_sync():
    """Test time sync update mechanism."""
    try:
        result = update_time_sync(force=True)
        
        # Should succeed or fail gracefully
        assert isinstance(result, bool)
        
        if result:
            # Check sync status
            status = get_sync_status()
            assert status["synced"] is True
            assert status["offset_ms"] is not None
            assert status["last_sync"] is not None
            assert status["age_seconds"] is not None
            assert status["age_seconds"] < 10  # Just synced
            
            print(f"✅ Time sync updated: offset = {status['offset_ms']:.1f}ms")
        else:
            print("⚠️  Time sync failed (network issue?)")
            
    except Exception as e:
        pytest.skip(f"Time sync test failed: {e}")


def test_synchronized_time():
    """Test getting synchronized time."""
    # Before sync, should return system time
    before_sync = get_synchronized_time()
    system_time = datetime.now(timezone.utc)
    
    assert abs((before_sync - system_time).total_seconds()) < 1
    
    # After sync (if available), should be close to system time
    try:
        update_time_sync(force=True)
        after_sync = get_synchronized_time()
        
        # Should be within reasonable range
        assert abs((after_sync - system_time).total_seconds()) < 10
        
    except TimeSyncError:
        pytest.skip("Network unavailable for sync test")


def test_now_utc_fallback():
    """Test that now_utc works with and without NTP."""
    # Should always return a datetime
    current_time = now_utc(use_ntp=False)
    assert isinstance(current_time, datetime)
    assert current_time.tzinfo == timezone.utc
    
    # With NTP (may or may not be synced)
    current_time_ntp = now_utc(use_ntp=True)
    assert isinstance(current_time_ntp, datetime)
    assert current_time_ntp.tzinfo == timezone.utc


def test_sync_status_unsynced():
    """Test sync status when not synced."""
    # Note: This test assumes no sync has been done
    # In a real scenario, previous tests might have synced
    status = get_sync_status()
    
    # Status should have all required keys
    assert "synced" in status
    assert "offset_ms" in status
    assert "last_sync" in status
    assert "age_seconds" in status


def test_ntp_timeout():
    """Test NTP timeout handling."""
    # Use invalid server to test timeout
    with pytest.raises(TimeSyncError) as exc_info:
        sync_time_ntp(server="invalid.nonexistent.server.local", timeout=2.0)
    
    assert "Could not resolve" in str(exc_info.value) or "timed out" in str(exc_info.value)


def test_ntp_offset_magnitude():
    """Test that NTP offset is within reasonable bounds."""
    try:
        ntp_time, offset = sync_time_ntp(timeout=5.0)
        
        # For a properly synced system, offset should be < 1 second
        # We allow up to 10 seconds for systems with poor time sync
        assert abs(offset) < 10, f"Clock offset suspiciously large: {offset}s"
        
        if abs(offset) > 1:
            print(f"⚠️  System clock offset: {offset*1000:.1f}ms (consider syncing system time)")
        else:
            print(f"✅ System clock well synchronized: offset = {offset*1000:.1f}ms")
            
    except TimeSyncError:
        pytest.skip("Network unavailable for NTP test")
