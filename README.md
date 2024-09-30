
# pAudio

`pAudio` is a Python wrapper for `paplay and parecord`, the PulseAudio command-line tool for playing and capturing audio data. This module allows you to use `parecord` directly from Python by passing options as function arguments.

## Installation

You can install the package via pip:

```
pip install paudio
```

## Example Usage

```
from pAudio import parecord

# Example of recording with specific options
output_file = "output.wav"
parecord(
    output_file=output_file,
    record=True,
    verbose=True,
    device="@DEFAULT_SOURCE@",
    rate=48000,  # Sample rate in Hz
    channels=1,  # Mono audio
    volume=32000,  # Mid-range volume
    raw=True  # Recording raw PCM data
)

```
