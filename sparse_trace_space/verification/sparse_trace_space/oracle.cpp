// Independent literal implementation: complete field, vector rotation, no macros.
#include <algorithm>
#include <fstream>
#include <iostream>
#include <set>
#include <string>
#include <utility>
#include <vector>
using namespace std;using P=pair<long long,long long>;
int main(int argc,char**argv){
 if(argc!=2){cerr<<"usage: oracle INPUT";return 2;}ifstream in(argv[1]);int cases;
 if(!(in>>cases)||cases<0||cases>10000)return 2;
 const P directions[]={{0,1},{1,0},{0,-1},{-1,0}};
 for(int cid=0;cid<cases;cid++){
  long long x,y;int h,n,m;if(!(in>>x>>y>>h>>n>>m)||h<0||h>3||n<0||n>1000000||m<0||m>10000)return 2;
  set<P>B,seen;for(int j=0;j<m;j++){P p;in>>p.first>>p.second;if(!B.insert(p).second)return 2;}
  long long dx=directions[h].first,dy=directions[h].second;string w;vector<int>firstblack;
  for(int t=0;t<n;t++){
   P p{x,y};bool b=B.count(p);if(!seen.count(p)&&b)firstblack.push_back(t);seen.insert(p);w.push_back(b?'L':'R');
   if(b)B.erase(p);else B.insert(p);long long u=dx;
   if(b){dx=-dy;dy=u;}else{dx=dy;dy=-u;}x+=dx;y+=dy;
  }
  for(h=0;h<4;h++)if(directions[h]==P{dx,dy})break;
  cout<<cid<<' '<<x<<' '<<y<<' '<<h<<' '<<B.size()<<'\n'<<w<<'\n';
  bool first=true;for(P p:B){if(!first)cout<<' ';first=false;cout<<p.first<<' '<<p.second;}cout<<'\n';
  first=true;for(int t:firstblack){if(!first)cout<<' ';first=false;cout<<t;}cout<<'\n';
 }
 if(!in){cerr<<"invalid input";return 2;}
}
