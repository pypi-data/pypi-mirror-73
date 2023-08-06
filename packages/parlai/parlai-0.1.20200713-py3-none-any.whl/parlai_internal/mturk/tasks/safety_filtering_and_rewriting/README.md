# Safety-filtering MTurk task

Main scripts, in the order in which they must be run:
- `run.py`: Master script for running HITs
- `remove_bad_reviews.py`: Remove the specified set of bad HITs from the stack
- `run.py`: Master script for running HITs (re-running after removing bad HITs above)

Helper scripts (in the `utils/` folder):
- `test_valid_responses.py`: Unit test of checks on valid/invalid responses to safety questions
- `aggregate_hits.py`: Compile results of HITs, including onboarding
- `remove_workers_from_stack.py`: Remove a list of workers from the stack
