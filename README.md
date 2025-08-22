# Astronomical-watch / Astronomski sat

English | [Srpski / Bosanski / Croatian](#srpski--bosanski--croatian)

---

## English

Astronomical-watch is an experimental timekeeping system that replaces the conventional calendar/time-of-day representation with one based on recurring astronomical phenomena:

1. Year boundary: moment of the (northern) vernal equinox.
2. Day index: counted from 0 up to 365 (or 366) across the interval between two consecutive vernal equinox instants.
3. Sub‑day unit: each day is divided into 1000 equal parts (000–999).  
   - One milli‑day = 86.4 seconds.
4. Day boundary: at (mean) astronomical noon at a fixed reference meridian located midway between Little Diomede Island (USA) and Big Diomede Island (Russia): 168° 58′ 30″ W.
5. Transition rules:
   - When the sub‑day counter rolls over 999 → 000, the day index increments.
   - When the vernal equinox occurs, the year day index resets to 0 regardless of the previous count (even if not yet at 365/366).
6. Required astronomy:
   - Precise calculation of vernal equinox instants (Meeus algorithms / solar apparent longitude = 0°).
   - Equation of Time (EoT) to relate apparent vs. mean solar time (for defining “mean astronomical noon” and optionally refining the start of day).

### Rationale

The tropical year (interval between two vernal equinoxes) has a relatively stable length (~365.2422 mean solar days). Using its natural boundaries avoids the Gregorian leap day machinery. Expressing intra‑year position as (day_index, milli_day) yields a uniform metric-like coordinate within each tropical year.

### Core Quantities

| Symbol | Meaning |
|--------|---------|
| T_eq_y | Exact UTC (or TT → then converted) instant of current year’s vernal equinox |
| T_eq_next | Exact instant of next vernal equinox |
| Y_len_days | (T_eq_next − T_eq_y) / 86400 (can be ~365.24…) |
| D_max | Integer number of full days in interval: round(T_eq_next − T_eq_y in days) → 365 or 366 |
| T_ref_meridian | Longitude λ_ref = −168° 58′ 30″ (decimal: −168.975°) |
| LMT (Local Mean Time) | UTC + λ_ref / 15 h |
| Mean noon | LMT = 12:00:00 |
| EoT | Apparent Solar Time − Mean Solar Time |
| Start of day | Mean local noon corrected per intended definition (see below) |

### Interpreting “start of day is mean astronomical noon (Equation of Time = 0)”

There are two possible interpretations; the project should clarify which to adopt:

1. Strict Mean Noon Interpretation (recommended initial implementation):
   - Start of each day occurs when Local Mean Solar Time (at λ_ref) = 12:00:00 (LMT noon).
   - EoT is computed only for optional display (showing difference to apparent solar time).

2. EoT Zero Crossing Interpretation:
   - Start of each day would be when EoT = 0 at the reference meridian (moments when apparent and mean solar time coincide). (Complication: EoT=0 occurs only ~4 times per tropical year → unsuitable for a daily boundary.)
   
Because the second interpretation cannot define daily boundaries, we proceed with (1). The README keeps the original note but clarifies operational meaning.

### Time Representation

We define an astronomical timestamp:

Year_Epoch = T_eq_y (UTC)
Now = t (UTC instant)

1. If t < T_eq_y, recompute for previous equinox.
2. Compute Δt = t − T_eq_y (seconds).
3. Compute day_index = floor( (t − T_eq_y − offset_to_first_noon) / 86400 ), where offset_to_first_noon aligns day 0 start to the first mean noon after the equinox (or at equinox if it falls before noon rule).
4. Compute intra_day_seconds = (t − start_of_current_day).
5. milli_day = floor( 1000 * intra_day_seconds / 86400 ). Range 000–999.
6. When milli_day rolls 999 → 000, day_index increments.
7. If t ≥ T_eq_next, reset day_index → 0 and recompute new frame.

Display Format (proposal):
YYYYeq:DDD.mmm
- YYYYeq: Gregorian year of the equinox starting the frame
- DDD: zero-padded day_index (e.g., 000–365/366)
- mmm: milli_day (000–999)

Example: 2025eq:123.457

### Algorithms Needed

1. Vernal Equinox Time (Meeus):
   - Use Jean Meeus “Astronomical Algorithms” Chapter for solar longitude.
   - Compute apparent solar longitude λ (corrected for nutation, aberration).
   - Find root of λ(t) − 0° (mod 360) near March equinox using iterative method (e.g., Newton-Raphson with derivative from mean motion ~0.9856°/day).
   - Higher precision: Evaluate in Terrestrial Time (TT); convert to UTC:
     UTC = TT − ΔT (ΔT can be approximated; store table or polynomial).

2. Equation of Time (EoT):
   - EoT = GHA_mean_sun − GHA_apparent_sun (or classical formula combining eccentricity and obliquity terms).
   - For display and (optionally) refining mean noon vs apparent noon.

3. Reference Meridian Mean Noon:
   - LMT = UTC + λ_ref / 15.
   - Mean noon occurs when LMT = 12:00. So:
     Start-of-day candidate = floor( (UTC + λ_ref / 15h) / 24h ) * 24h − λ_ref / 15h + 12h
   - Ensure start-of-day ≥ T_eq_y for day 0. If equinox occurs after that day's noon, use next day’s noon as start-of-day.

### Handling Day Count (365 vs 366)

Because the tropical year length is ~365.2422 days:

- Compute int_days = floor( (T_eq_next − T_eq_y) / 86400 ) → usually 365.
- If fractional remainder + alignment with noon boundaries pushes number of distinct day starts to 366, then D_max=366.
- Accept that final day may have fewer milli-day units if the equinox truncates it; or, alternatively, re-scale the last day (OPTION A vs OPTION B):

Option A (simpler): Truncate final day at next equinox (last milli_day may not reach 999).  
Option B (normalized): Stretch scaling on each day to ensure full 1000 milli-days (complicates uniformity).  
We choose Option A initially.

### Precision Targets

| Quantity | Target Accuracy | Method |
|----------|-----------------|--------|
| Equinox instant | < 1 minute | Meeus low-order + iteration |
| EoT | < few seconds | Standard simplified formula |
| Day boundary alignment | < 1 second | Use high-resolution time libs |

### Implementation Plan

1. Core library:
   - Language: (To be decided; e.g., Python/TypeScript/Rust).
   - Module: solar.py / solar.ts for Sun position & EoT.
   - Function: compute_vernal_equinox(year) -> datetime (UTC).
   - Function: astronomical_now(t_utc) -> {equinox_epoch, next_equinox, day_index, milli_day, raw_fraction, eot, metadata}.
2. CLI Tool:
   - astronomical-watch now → prints current astronomical timestamp.
3. Tests:
   - Compare equinox times to published tables (e.g., NASA) within tolerance.
4. Future UI:
   - Web viz: Circular dial 0–999; year progress bar 0–365(6).
   - Option to show difference to civil time (UTC offset).

### Example Pseudocode (High-Level)

```python
t = now_utc()

eq = compute_vernal_equinox(frame_year_guess(t))
next_eq = compute_vernal_equinox(frame_year_guess(t)+1)

if t < eq:
    # Use previous frame
    eq = compute_vernal_equinox(frame_year_guess(t)-1)
    next_eq = compute_vernal_equinox(frame_year_guess(t))

day0_start = first_mean_noon_at_or_after(eq, lambda_ref)

# Compute current day start
days_since_day0 = floor((t - day0_start)/DAY_SECONDS)
current_day_start = day0_start + days_since_day0 * DAY_SECONDS

if t >= next_eq:
    rollover...

intra = t - current_day_start
milli_day = int((intra / DAY_SECONDS) * 1000)  # clamp 0..999

timestamp = f"{eq.year}eq:{days_since_day0:03d}.{milli_day:03d}"
```

### Open Questions

- Confirm interpretation of “Equation of time = 0” in original definition.
- Decide library language.
- Decide handling of partial last day.
- Will we expose ΔT configuration for higher precision?

---

## Srpski / Bosanski / Croatian

Astronomical-watch je eksperimentalni sistem mjerenja vremena koji zamjenjuje klasičan kalendar i sat prikazom zasnovanim na ponavljajućim astronomskim pojavama:

1. Granica godine: trenutak sjeverne proljetne (prolećne) ravnodnevnice.
2. Broj dana: broje se od 0 do 365 (ili 366) unutar intervala između dvije uzastopne proljetne ravnodnevnice.
3. Podjela dana: svaki dan se dijeli na 1000 jednakih dijelova (000–999).
   - Jedna hiljaditina dana = 86,4 sekundi.
4. Početak dana: srednje astronomsko podne na referentnom meridijanu između američkog Diomede (Little Diomede) i ruskog Diomede (Big Diomede): 168° 58′ 30″ W.
5. Pravila prelaza:
   - Kad se 999 → 000, dan se povećava za 1.
   - Kad nastupi proljetna ravnodnevnica, dan se resetuje na 0 (počinje nova astronomska godina).
6. Potrebni proračuni:
   - Tačan trenutak proljetne ravnodnevnice (Meeus).
   - Jednačina vremena (Equation of Time) za odnos prividnog i srednjeg solarnog vremena.

### Obrazloženje

Tropska godina (između ravnodnevnica) je relativno stabilna (~365,2422 dana). Korištenje njenih prirodnih granica eliminiše potrebu za gregorijanskim prestupnim pravilima na prikazu.

### Ključne veličine

(Analogno engleskom dijelu; zadržavamo simbole radi jednoznačnosti.)

### Tumačenje “početak dana je srednje astronomsko podne (Equation of Time = 0)”

Praktično ćemo uzeti da je početak dana srednje solarno podne po lokalnom srednjem vremenu referentnog meridijana (jer EoT=0 se javlja samo ~4 puta godišnje, što nije pogodno za dnevnu granicu).

### Reprezentacija vremena

Format: YYYYeq:DDD.mmm (npr. 2025eq:123.457)

### Algoritmi

- Meeus za Sunce i ravnodnevnicu (solar longitude = 0°).
- Jednačina vremena standardnom formulom.

### Plan implementacije

1. Biblioteka za proračune.
2. CLI alat (npr. `astronomical-watch now`).
3. Testovi naspram referentnih tabela (npr. NASA).
4. Vizualizacija (dijal 0–999; progres godine).

### Otvorena pitanja

- Da li strogo treba korigovati početak prvog dana ako je ravnodnevnica poslije podneva?
- Kako tretirati nepotpun zadnji dan (prijedlog: dozvoliti trunciranje)?

---

## Contributing

(Placeholder — to be expanded.)

## License

(Choose a suitable license: e.g., MIT / Apache-2.0.)

---

## Next Steps

- Decide primary language (code).
- Implement equinox + EoT functions.
- Implement core conversion to (day_index, milli_day).
- Add tests.
- Publish first CLI.
