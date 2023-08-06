from typing import Any, Callable, List
import colorama
import traceback


class TestCases:
    @classmethod
    def run(cls, solution: Any):
        instance = cls()
        tests = instance._find_tests()
        print(f"{colorama.Fore.WHITE}Running {len(tests)} tests")
        passed = instance._run_tests(tests, solution)
        print(f"{colorama.Fore.WHITE}{passed} of {len(tests)} tests passed")
        print(colorama.Style.RESET_ALL)

    def _run_test(self, test: Any, solution: Any) -> bool:
        try:
            test(solution)
        except AssertionError:
            print(f"{colorama.Fore.RED}{test.__name__} failed [incorrect result]", flush=True)
        except Exception as error:
            print(f"{colorama.Fore.WHITE}{'-' * 60}", flush=True)
            print(f"{colorama.Fore.RED}{test.__name__} failed [with an exception]{colorama.Fore.YELLOW}", flush=True)
            traceback.print_exc()
            print(colorama.Fore.WHITE, "-" * 60, sep="", flush=True)
        else:
            print(f"{colorama.Fore.GREEN}{test.__name__} passed", flush=True)
            return True
        finally:
            print(colorama.Style.RESET_ALL, flush=True, end="")
        return False

    def _run_tests(self, tests: List[Callable], solution: Callable) -> int:
        passed = 0
        for test in tests:
            passed += self._run_test(test, solution)
        return passed

    def _find_tests(self) -> List[Callable]:
        return [
            getattr(self, name)
            for name in self.__class__.__dict__
            if name.startswith("test_") and callable(getattr(self, name))
        ]
