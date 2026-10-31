// Independent bit-packed complete-field simulator and all-epoch tail check.
// Compiles with C++17; no generated transition graph is consulted.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <set>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>
using namespace std;
using P=pair<int,int>; using Field=unordered_set<uint64_t>;
uint64_t key(P p){return (uint64_t(uint32_t(p.first))<<32)|uint32_t(p.second);}
P decode(uint64_t z){return {int32_t(z>>32),int32_t(z)};}
P direction[]={{0,1},{1,0},{0,-1},{-1,0}};
struct Pose {int x,y,h;};
char step(Field& b,Pose& p){
 auto q=key({p.x,p.y});bool black=b.count(q);
 if(black)b.erase(q);else b.insert(q);
 p.h=(p.h+(black?3:1))%4;p.x+=direction[p.h].first;p.y+=direction[p.h].second;
 return black?'L':'R';
}
vector<P> sorted_field(const Field& b){vector<P>out;for(auto q:b)out.push_back(decode(q));sort(out.begin(),out.end());return out;}
void print_field(const vector<P>&b){cout<<'[';bool comma=false;for(auto p:b){if(comma)cout<<',';comma=true;cout<<'['<<p.first<<','<<p.second<<']';}cout<<']';}
void print_pose(Pose p){cout<<'['<<p.x<<','<<p.y<<','<<p.h<<']';}
int multiple(P a,P d){
 int den=d.first?d.first:d.second;int num=d.first?a.first:a.second;
 if(!den||num%den)return numeric_limits<int>::min();int t=num/den;
 return a==P{t*d.first,t*d.second}?t:numeric_limits<int>::min();
}
bool forever(const Field& B,Pose root,const string&w){
 vector<P>reads;Pose p=root;
 for(char c:w){reads.push_back({p.x,p.y});p.h=(p.h+(c=='R'?1:3))%4;p.x+=direction[p.h].first;p.y+=direction[p.h].second;}
 P d={p.x-root.x,p.y-root.y};if(p.h!=root.h||d==P{0,0})return false;
 for(int i=0;i<int(w.size());i++){
  vector<int>toggle;
  if(w[i]=='L')toggle.push_back(0);
  for(int j=0;j<int(w.size());j++){
   int n=multiple({reads[j].first-reads[i].first,reads[j].second-reads[i].second},d);
   if(n>0||(n==0&&j<i))toggle.push_back(n);
  }
  for(auto raw:B){P q=decode(raw);int n=multiple({q.first-reads[i].first,q.second-reads[i].second},d);
   if(n>=0){toggle.push_back(n);toggle.push_back(n+1);}
  }
  sort(toggle.begin(),toggle.end());
  for(size_t j=0;j<toggle.size();){size_t end=j+1;while(end<toggle.size()&&toggle[end]==toggle[j])end++;
   if((end-j)%2)return false;j=end;}
 }
 return true;
}
void append(vector<int>& v,const vector<int>&p,int n){for(int j=0;j<n;j++)v.insert(v.end(),p.begin(),p.end());}
int main(int argc,char**argv){
 try{
  if(argc!=2)throw runtime_error("usage: independent INPUT");ifstream f(argv[1]);int tests;f>>tests;
  if(!f||tests<0||tests>2000)throw runtime_error("bad input count");
  while(tests--){int l,r;long long tau;f>>l>>r>>tau;
   if(!f||l<0||r<0||l>5000||r>5000||tau<1||tau>20000000)throw runtime_error("unsupported resource bounds");
   vector<int>left{5},columns;append(left,{6,10,12,17},1);append(left,{18,29},l);
   for(auto it=left.rbegin();it!=left.rend();it++)columns.push_back(31-*it);
   append(columns,{6,10,12,17},1);append(columns,{18,29},r);int width=columns.size();
   Field B;B.reserve(50000);for(int x=0;x<width;x++)for(int y=0;y<5;y++)if(columns[x]>>y&1)B.insert(key({x,y}));
   Pose p{2*l+5,3,1},at_exit{},at_entry{};vector<P>exit_field,entry_field;Field entry;
   string trace;trace.reserve(tau+104);long long exit_time=-1;
   for(long long t=0;t<tau+104;t++){
    trace.push_back(step(B,p));
    if(exit_time<0&&!(0<=p.x&&p.x<width&&0<=p.y&&p.y<5)){
     exit_time=t+1;at_exit=p;exit_field=sorted_field(B);
    }
    if(t+1==tau){entry=B;at_entry=p;entry_field=sorted_field(B);}
   }
   string word=trace.substr(tau);bool accepted=forever(entry,at_entry,word);
   cout<<"{\"l\":"<<l<<",\"r\":"<<r<<",\"first_exit\":"<<exit_time<<",\"exit_pose\":";print_pose(at_exit);
   cout<<",\"exit_field\":";print_field(exit_field);cout<<",\"entry_pose\":";print_pose(at_entry);
   cout<<",\"entry_field\":";print_field(entry_field);cout<<",\"turns\":\""<<trace<<"\",\"tail_accepted\":"<<(accepted?"true":"false")<<"}\n";
  }
 }catch(const exception&e){cerr<<e.what()<<'\n';return 2;}
}
