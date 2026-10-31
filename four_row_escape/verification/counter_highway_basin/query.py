"""Evaluate the proved two-counter entry law, not a generic HC decision tool."""
import argparse
import json
from core import prediction,max_entry_at_minimum

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('left',type=int);parser.add_argument('right',type=int)
args=parser.parse_args()
try:
    exit_time,recovery,entry=prediction(args.left,args.right)
except ValueError as exc:parser.error(str(exc))
print(json.dumps({'left':args.left,'right':args.right,
                  'input':'J((5) C V^left) C V^right; root=(2left+5,3),E; white elsewhere',
                  'initial_black':4*args.left+6*args.right+23,
                  'width':2*(args.left+args.right)+9,
                  'first_rectangle_exit':exit_time,'post_exit_recovery':recovery,
                  'first_permanent_P104':entry,
                  'worst_P104_entry_at_this_smaller_counter':max_entry_at_minimum(min(args.left,args.right)),
                  'literal_simulation_performed':False},indent=2))
