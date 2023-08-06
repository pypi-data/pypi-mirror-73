from typing import Any, Callable
import importlib


def run_tests(solution: Any, challenge: str):
    tests = importlib.import_module(f"beginnerpy.challenges.{challenge}.tests")
    tests.Tests.run(solution)
