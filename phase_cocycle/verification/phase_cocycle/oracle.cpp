// Independent ordinary dynamics and pose-potential construction on the 4x4 graph.
// No Python head-potential formula, path integration, or historical ant module.
#include <array>
#include <deque>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>
using namespace std;
using Point=pair<long long,long long>;
int mod(long long x,int m){int r=int(x%m);return r<0?r+m:r;}
const int dx[4]={0,1,0,-1},dy[4]={1,0,-1,0};
struct Clock {
 string rule; int n,r,m; bool common; array<int,64> phi;
 vector<int> rp,lp;
 Clock(string w,bool use_common):rule(w),n(int(w.size())),r(0),common(use_common){
  for(char c:rule){if(c!='R'&&c!='L')throw runtime_error("bad rule");r+=(c=='R');}
  m=((!common&&(r%2)&&((n-r)%2))?8:4)*n;
  rp.push_back(0);lp.push_back(0);
  for(char c:rule){rp.push_back(rp.back()+(c=='R'));lp.push_back(lp.back()+(c=='L'));}
  phi.fill(-1);phi[0]=0;deque<int> q;q.push_back(0);
  while(!q.empty()){
   int v=q.front();q.pop_front();int h=v%4,y=(v/4)%4,x=v/16;
   for(int s:{1,-1}){
    int hh=mod(h+s,4),xx=mod(x+dx[hh],4),yy=mod(y+dy[hh],4);
    int u=16*xx+4*yy+hh;auto [a,b]=increments(x,y);
    int value=mod(phi[v]+1-(s==1?a:b),m);
    if(phi[u]<0){phi[u]=value;q.push_back(u);}else if(phi[u]!=value)throw runtime_error("nonzero pose circulation");
   }
  }
  for(int x=0;x<4;x++)for(int y=0;y<4;y++)for(int h=0;h<4;h++)
   if(mod(h-x-y,2)==0&&phi[16*x+4*y+h]<0)throw runtime_error("uncovered pose");
 }
 pair<int,int> increments(long long x0,long long y0) const{
  int x=mod(x0,4),y=mod(y0,4),a,b;
  if(!common&&(r%2)&&((n-r)%2)){
   int chi=((x+y)%2)?-1:1;
   a=4*((1-n/2)*(x%2)*(y%2)-(n/2)*chi*x*y);b=(1-n)*a;
  }else a=b=4*(x%2)*(y%2);
  return {mod(a,m),mod(b,m)};
 }
 Point rotate(Point p,int sector)const{return sector?Point{-p.second,p.first}:p;}
 int cell(Point p,int color,int sector) const {
  if(color<0||color>=n)throw runtime_error("bad color");
  p=rotate(p,sector);auto [a,b]=increments(p.first,p.second);
  return mod(rp[color]*a+lp[color]*b,m);
 }
 int pose(Point p,int h,int sector) const {
  p=rotate(p,sector);h=mod(h-sector,4);
  return phi[16*mod(p.first,4)+4*mod(p.second,4)+h];
 }
 int field(const map<Point,int>&B,int sector)const{int z=0;for(auto [p,c]:B)z=mod(z+cell(p,c,sector),m);return z;}
};
int main(int argc,char**argv){
 try{
  if(argc!=2)throw runtime_error("usage: oracle INPUT");ifstream in(argv[1]);int count;if(!(in>>count)||count<0)throw runtime_error("bad case count");
  for(int id=0;id<count;id++){
   string rule;long long x,y;int h,steps,k;in>>rule>>x>>y>>h>>steps>>k;
   if(!in||rule.empty()||h<0||h>3||steps<0||k<0)throw runtime_error("malformed case");
   map<Point,int>B;for(int i=0;i<k;i++){long long xx,yy;int c;in>>xx>>yy>>c;if(!c||c>=int(rule.size()))throw runtime_error("bad initial color");B[{xx,yy}]=c;}
   Clock a(rule,false),g(rule,true);Point p{x,y};int sector=mod(h-x-y,2);
   int af=a.field(B,sector),gf=g.field(B,sector),initial=mod(af+a.pose(p,h,sector),a.m),gi=mod(gf+g.pose(p,h,sector),g.m);
   string colors;colors.reserve(steps);
   for(int t=0;t<steps;t++){
    int c=B.count(p)?B[p]:0;colors.push_back(char('A'+c));int nc=(c+1)%int(rule.size());
    af=mod(af+a.cell(p,nc,sector)-a.cell(p,c,sector),a.m);gf=mod(gf+g.cell(p,nc,sector)-g.cell(p,c,sector),g.m);
    if(nc)B[p]=nc;else B.erase(p);
    h=mod(h+(rule[c]=='R'?1:-1),4);p.first+=dx[h];p.second+=dy[h];
    if(mod(af+a.pose(p,h,sector)-initial,a.m)!=(t+1)%a.m)throw runtime_error("clock failure");
    if(mod(gf+g.pose(p,h,sector)-gi,g.m)!=(t+1)%g.m)throw runtime_error("common clock failure");
    if(t%97==0&&(a.field(B,sector)!=af||g.field(B,sector)!=gf))throw runtime_error("complete field mismatch");
   }
   cout<<id<<' '<<p.first<<' '<<p.second<<' '<<h<<' '<<initial<<' '<<mod(af+a.pose(p,h,sector),a.m)<<' '<<gi<<' '<<mod(gf+g.pose(p,h,sector),g.m)<<' '<<B.size()<<'\n';
   cout<<colors<<'\n';for(auto [q,c]:B)cout<<q.first<<' '<<q.second<<' '<<c<<' ';cout<<'\n';
  }
 }catch(const exception&e){cerr<<e.what()<<'\n';return 2;}
}
