import importlib
import importlib.util
import os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path


def run_app(app: str):
    os.system(f"python {app}")


def main():
    app_paths = [p for p in Path("./examples").rglob("*.py")]

    with ProcessPoolExecutor() as executor:
        for ap in app_paths:
            spec = importlib.util.spec_from_file_location(f"{ap.stem}", ap)
            app = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(app)
            if app.RUN:
                print("running app:", app)
                executor.submit(run_app, ap)


if __name__ == "__main__":
    main()
