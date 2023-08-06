from typing import Callable
import importlib


def run_tests(function: Callable, challenge: str):
    tests = importlib.import_module(f"beginnerpy.challenges.{challenge}.tests")
    test_case = tests.Tests()
    test_case.set_solution_function(function)
    test_case.run()


run_tests(lambda self: True, "adventure_game")
