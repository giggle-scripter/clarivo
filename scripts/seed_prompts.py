from pathlib import Path
import sys


API_ROOT = Path(__file__).resolve().parents[1] / "apps" / "api"
sys.path.insert(0, str(API_ROOT))

from app.db.seed import main  # noqa: E402


if __name__ == "__main__":
    main()
