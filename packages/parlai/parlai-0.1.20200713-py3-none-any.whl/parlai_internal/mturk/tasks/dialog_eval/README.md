# DialogEval MTurking

[Takeaway from two mid sized runs (600+hits).](https://fb.quip.com/CwzXA7JeXmzH)

### Additional note

I was running with this patch on the former MTurk Manager (I believe it has been refactored since).
The first change allows workers to rate each other in the human human without one disconnecting affecting the other's ranking.
The second is just for debugging processes since it can be quite long to reach this useless halt (useless for debugging) before another long waiting time.

```diff
diff --git a/parlai/mturk/core/mturk_manager.py b/parlai/mturk/core/mturk_manager.py
index 43daffb..2f16e32 100644
--- a/parlai/mturk/core/mturk_manager.py
+++ b/parlai/mturk/core/mturk_manager.py
@@ -581,7 +581,7 @@ class MTurkManager():
         agent = self._get_agent(worker_id, assignment_id)
         if agent is None:
             self._log_missing_agent(worker_id, assignment_id)
-        elif not agent.state.is_final():
+        else:
             shared_utils.print_and_log(
                 logging.INFO,
                 'Manager received: {}'.format(pkt),
@@ -781,7 +781,7 @@ class MTurkManager():
                 ''.format(HIT_MULT, fin_word),
                 should_print=True,
             )
-        input('Please press Enter to continue... ')
+        # input('Please press Enter to continue... ')
         shared_utils.print_and_log(logging.NOTSET, '', True)
 
         if self.opt['local'] is True:
```