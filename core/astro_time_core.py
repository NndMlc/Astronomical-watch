from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Optional

# Reference meridian (decimal degrees, West negative). Provided by project specification.
LONGITUDE_REF_DEG: float = -168.975  # -168° 58′ 30″

# Local Mean Time (LMT) = UTC + LONGITUDE/15 h.
# For the reference longitude this is an offset of about -11.265 hours, meaning that when
# local mean time is 12:00:00, UTC is approximately 23:15:54.
NOON_UTC_HOUR: int = 23
NOON_UTC_MINUTE: int = 15
NOON_UTC_SECOND: int = 54

# Sub‑day subdivision.
MILIDIES_PER_DAY: int = 1000
SECONDS_PER_DAY: int = 86400
SECONDS_PER_MILIDIES: float = SECONDS_PER_DAY / MILIDIES_PER_DAY  # 86.4 seconds

# Legacy compatibility constants (aliases – keep until full migration).
MILLIDAN_PER_DAY = MILIDIES_PER_DAY  # legacy name
SECONDS_PER_MILLIDIES = SECONDS_PER_MILIDIES  # spelled from original draft

dataclass(frozen=True)
class AstroReading:
    """Snapshot of astronomical time representation.

    Attributes:
        utc: Original UTC instant.
        dies: Day index within the astronomical (tropical) year, starting at 0.
        milidies: Subdivision of the current day (0..999).
        fraction: Floating fraction of the day in [0.0, 1.0) matching milidies / 1000 plus remainder.

    Deprecated alias properties (day_index, milidan) are provided for transitional compatibility.
    They intentionally emit no warnings yet; a future PR may introduce DeprecationWarning.
    """
    utc: datetime
    dies: int
    milidies: int
    fraction: float

    # Deprecated aliases --------------------------------------------------
    @property
    def day_index(self) -> int:  # legacy
        return self.dies

    @property
    def milidan(self) -> int:  # legacy
        return self.milidies

class AstroYear:
    """Encapsulates an astronomical year bounded by vernal equinox instants.

    Day boundaries are defined by the reference meridian's mean noon, which corresponds
    to a fixed UTC clock time of 23:15:54. The *first* boundary *after* the vernal equinox
    begins dies=1; the interval from the equinox instant up to that boundary is dies=0.
    Subsequent days are uniform 86400 s segments each subdivided into 1000 milidies.

    The length of dies=0 may be shorter or longer than a full day depending on the equinox
    instant. We still map its intra‑day progress onto the 0..999 milidies range for simplicity.
    """

    def __init__(self, current_equinox: datetime, next_equinox: datetime):
        if current_equinox.tzinfo is None or next_equinox.tzinfo is None:
            raise ValueError("Equinox datetimes must be timezone-aware (UTC)")
        if current_equinox >= next_equinox:
            raise ValueError("next_equinox must be after current_equinox")
        if current_equinox.tzinfo != timezone.utc or next_equinox.tzinfo != timezone.utc:
            raise ValueError("Equinox datetimes must be in UTC")
        self.current_equinox = current_equinox
        self.next_equinox = next_equinox
        # Pre-compute the first noon boundary after current equinox.
        self.first_noon_after_equinox = self._compute_first_noon_after(current_equinox)

    # ------------------------------------------------------------------
    @staticmethod
    def _compute_first_noon_after(instant: datetime) -> datetime:
        # Compute the UTC datetime of the next (or same if strictly later) reference noon after 'instant'.
        candidate = instant.replace(hour=NOON_UTC_HOUR, minute=NOON_UTC_MINUTE, second=NOON_UTC_SECOND, microsecond=0)
        if candidate <= instant:
            candidate += timedelta(days=1)
        return candidate

    # ------------------------------------------------------------------
    def to_reading(self, t: datetime) -> AstroReading:
        """Produce an AstroReading for UTC instant t (auto-handles rollover if needed)."""
        if t.tzinfo is None:
            raise ValueError("Input datetime must be timezone-aware UTC")
        if t.tzinfo != timezone.utc:
            raise ValueError("Input datetime must be UTC")

        # Rollover if t is beyond current astronomical year.
        if t >= self.next_equinox:
            raise ValueError("Instant beyond this AstroYear's range – construct a new AstroYear")

        if t < self.first_noon_after_equinox:
            dies = 0
            day_start = self.current_equinox
        else:
            delta = t - self.first_noon_after_equinox
            complete_days = int(delta.total_seconds() // SECONDS_PER_DAY)
            dies = 1 + complete_days
            day_start = self.first_noon_after_equinox + timedelta(days=complete_days)

        intra_seconds = (t - day_start).total_seconds()
        # Clamp potential floating errors just below 86400.
        if intra_seconds < 0:
            intra_seconds = 0.0
        if intra_seconds >= SECONDS_PER_DAY:
            intra_seconds = SECONDS_PER_DAY - 1e-9

        milidies = int((intra_seconds / SECONDS_PER_DAY) * MILIDIES_PER_DAY)
        fraction = intra_seconds / SECONDS_PER_DAY

        return AstroReading(utc=t, dies=dies, milidies=milidies, fraction=fraction)

    # Legacy alias -----------------------------------------------------
    def to_legacy_reading(self, t: datetime) -> AstroReading:
        return self.to_reading(t)

    # ------------------------------------------------------------------
    def approximate_utc_from_dies_milidies(self, dies: int, milidies: int) -> datetime:
        """Approximate UTC instant for given dies & milidies within this astronomical year.

        For dies=0 we map milidies over a synthetic 86400 s span starting at the equinox.
        For dies>=1 we map day spans of exactly 86400 s beginning at the first noon boundary.
        Raises ValueError if dies would exceed the year span.
        """
        if dies < 0:
            raise ValueError("dies must be >= 0")
        if not (0 <= milidies < MILIDIES_PER_DAY):
            raise ValueError("milidies out of range 0..999")

        if dies == 0:
            base = self.current_equinox
        else:
            base = self.first_noon_after_equinox + timedelta(days=dies - 1)

        approx = base + timedelta(seconds=(milidies + 0.5) * SECONDS_PER_MILIDIES)
        if approx >= self.next_equinox:
            raise ValueError("(dies, milidies) outside this astronomical year")
        return approx

    # Legacy alias name -------------------------------------------------
    def approximate_utc_from_day_milidan(self, day_index: int, milidan: int) -> datetime:
        return self.approximate_utc_from_dies_milidies(day_index, milidan)

    # Convenience -------------------------------------------------------
    @classmethod
    def from_equinoxes(cls, current_equinox: datetime, next_equinox: datetime) -> 'AstroYear':
        return cls(current_equinox, next_equinox)
