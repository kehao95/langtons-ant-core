// Independent complete finite-word enumeration: depth-first reversible cell map.
// The Python implementation is breadth-first with copied last-read maps.
#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <utility>
#include <vector>
#include <cstdlib>
using namespace std;
const string W="RRLLLLRLRRRRLRRRRLLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRL"
               "LRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRR";
array<bool,1024> allowed{};
map<pair<int,int>,int> last;
vector<string> leaves;
array<unsigned long long,151> counts{};
int short_radius=0;
string word;
void dfs(int x,int y,int dx,int dy,int history,int depth){
 ++counts[depth];
 if(depth<=149)short_radius=max(short_radius,max(abs(x),abs(y)));
 if(depth==150){leaves.push_back(word);return;}
 auto p=make_pair(x,y);auto old=last.find(p);int saved=old==last.end()?-1:old->second;
 for(int bit: {1,0}){ // L then R, not the Python bit order.
  int next=((history<<1)|bit)&1023;
  if(depth>=9 && !allowed[next])continue;
  if(saved==bit)continue;
  int ux=bit?-dy:dy,uy=bit?dx:-dx;
  last[p]=bit;word.push_back(bit?'L':'R');
  dfs(x+ux,y+uy,ux,uy,next,depth+1);word.pop_back();
  if(saved<0)last.erase(p);else last[p]=saved;
 }
}
int main(int argc,char**argv){
 if(argc!=3){cerr<<"usage: enum words.txt stats.json\n";return 2;}
 if(W.size()!=104)return 3;
 for(int i=0;i<104;++i){int k=0;for(int j=0;j<10;++j)k=(k<<1)|(W[(i+j)%104]=='L');allowed[k]=true;}
 dfs(0,0,0,1,0,0);sort(leaves.begin(),leaves.end());
 ofstream f(argv[1]);for(const auto&w:leaves)f<<w<<'\n';
 ofstream s(argv[2]);s<<"{\"word_count\":"<<leaves.size()<<",\"short_radius\":"<<short_radius<<",\"counts\":[";
 for(int i=0;i<=150;++i){if(i)s<<',';s<<counts[i];}s<<"]}\n";
 if(!f||!s)return 4;
 return 0;
}
