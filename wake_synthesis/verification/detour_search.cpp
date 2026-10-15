// Bounded experiment only. The complete run is maxlen=28; no HC or
// all-period exclusion follows. Standard word is REQUIRED as argv[2].
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <string>
#include <vector>
using namespace std;
struct Q{int x,y;};
const int dx[4]={0,1,0,-1},dy[4]={1,0,-1,0};
string W;
struct E{int key1,key2,ord,bit;bool operator<(const E&o)const{return tie(key1,key2,ord)<tie(o.key1,o.key2,o.ord);}};
bool valid(const string&w){int n=w.size(),x=0,y=0,h=0;vector<Q>p;for(char c:w){p.push_back({x,y});h=(h+(c=='R'?1:3))%4;x+=dx[h];y+=dy[h];}if(h||(!x&&!y))return false;vector<E>ev;for(int i=0;i<n;i++){int u=p[i].x,v=p[i].y;if(x){int a=(u-(u%abs(x)+abs(x))%abs(x))/x;ev.push_back({y*u-x*v,(u%abs(x)+abs(x))%abs(x),i-a*n,w[i]=='L'});}else{int a=(v-(v%abs(y)+abs(y))%abs(y))/y;ev.push_back({u,(v%abs(y)+abs(y))%abs(y),i-a*n,w[i]=='L'});}}sort(ev.begin(),ev.end());int expected=0,k1=0,k2=0;bool first=true;for(auto&e:ev){if(first||e.key1!=k1||e.key2!=k2)expected=0;if(e.bit!=expected)return false;expected^=1;k1=e.key1;k2=e.key2;first=false;}return true;}
uint64_t loops=0,tested=0;int maxlen;vector<string>hits;
void visit(int x,int y,int h,string &s,vector<array<int,3>>&hist){int len=s.size();if(len&&len%4==0&&!x&&!y&&!h){loops++;for(int i=0;i<104;i++){string c=W.substr(0,i)+s+W.substr(i);tested++;if(valid(c)){cout<<"HIT "<<len<<" "<<i<<" "<<c<<endl;hits.push_back(c);}}}if(len==maxlen)return;
// A finite inserted fragment must alternate reads at each repeated coordinate.
int prev=-1;for(int i=(int)hist.size()-1;i>=0;i--)if(hist[i][0]==x&&hist[i][1]==y){prev=hist[i][2];break;}
for(int b=0;b<2;b++){if(b==prev)continue;int hh=(h+(b?3:1))%4;int xx=x+dx[hh],yy=y+dy[hh];if(abs(xx)+abs(yy)>maxlen-len-1)continue;hist.push_back({x,y,b});s.push_back(b?'L':'R');visit(xx,yy,hh,s,hist);s.pop_back();hist.pop_back();}}
int main(int argc,char**argv){if(argc<3)return 2;maxlen=stoi(argv[1]);W=argv[2];if(W.size()!=104||!valid(W)){cerr<<"BAD STANDARD\n";return 3;}string s;vector<array<int,3>>hist;visit(0,0,0,s,hist);cerr<<"loops="<<loops<<" tests="<<tested<<" hits="<<hits.size()<<"\n";}
