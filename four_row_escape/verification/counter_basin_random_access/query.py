"""Exact whole-state queries for the certified two-counter source, not general HC."""
import argparse
import json
from core import state_at

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('left',type=int)
parser.add_argument('right',type=int)
parser.add_argument('time',type=int)
parser.add_argument('--cell',type=int,nargs=2,action='append',default=[],metavar=('X','Y'))
parser.add_argument('--toggle',type=int,nargs=2,action='append',default=[],metavar=('X','Y'),
                    help='initial XOR flip, accepted only in a proved unread half-strip')
parser.add_argument('--field',action='store_true',help='include the complete XOR-segment representation')
args=parser.parse_args()
try:
    result=state_at(args.left,args.right,args.time,protected_toggles=args.toggle)
    report={'source_family':'J((5)CV^left)CV^right; complete white exterior except accepted toggles',
            'time':args.time,'pose':list(result.pose),'heading_names':['N','E','S','W'],
            'stage':result.phase,'first_exit':result.first_exit,
            'first_permanent_P104':result.first_standard,
            'complete_black_mass':result.field.cardinality(),'next_turn':result.next_turn(),
            'cell_colors':[{'point':q,'black':result.field.contains(q)}for q in args.cell],
            'statistics':result.stats,'representation':'XOR of finite [x,y,dx,dy,count] segments',
            'is_generic_HC_solver':False}
    if args.field:report['complete_field']=result.field.as_lists()
except (ValueError,RuntimeError)as exc:parser.error(str(exc))
print(json.dumps(report,sort_keys=True,indent=2))
