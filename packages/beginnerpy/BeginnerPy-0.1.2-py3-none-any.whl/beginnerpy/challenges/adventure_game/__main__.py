from beginnerpy.challenges.adventure_game.tests import run_tests
import datetime
import random


random.seed(datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
run_tests()
