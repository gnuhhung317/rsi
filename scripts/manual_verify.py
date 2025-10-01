from pprint import pprint
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app import _compute_rsi


CASES = {
    "all_gains": {
        "prices": [1, 2, 3, 4, 5, 6],
        "lookback": 3,
    },
    "all_losses": {
        "prices": [6, 5, 4, 3, 2, 1],
        "lookback": 3,
    },
    "flat": {
        "prices": [4, 4, 4, 4, 4, 4],
        "lookback": 3,
    },
    "mixed_short": {
        "prices": [10, 11, 12, 11, 12, 10, 13],
        "lookback": 2,
    },
}


for name, params in CASES.items():
    print(f"\n{name}")
    result = _compute_rsi(params["prices"], params["lookback"])
    pprint(list(result))
