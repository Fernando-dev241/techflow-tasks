"""Ponto de entrada: inicia o servidor de desenvolvimento."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from techflow.app import create_app  # noqa: E402

if __name__ == "__main__":
    create_app().run(debug=True)
