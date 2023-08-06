# Random Candidate

Agent that calculates the distribution of labels on the train set, then during eval time selects a candidate randomly from the set based on this distribution. For instance, if in the train set 40% of labels were X and 60% of labels were Y, during evaluation it would choose label X with probability 0.4 and Y with probability 0.6.

## Basic Examples

Evaluate on dialogue safety by choosing a random candidate according to the distribution of labels in the train set.
```bash
python eval_model.py -t dialogue_safety -m internal:random_candidate_distribution
```
