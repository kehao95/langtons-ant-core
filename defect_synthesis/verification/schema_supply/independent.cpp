// Literal vector-rotation execution from a complete minimal input, not ISL.
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <utility>
#include <vector>
using Pt=std::pair<long long,long long>;
int main(){
 std::string W; if(!(std::cin>>W)) return 1;
 std::set<std::string> legal;std::string ww=W+W;
 for(int i=0;i<104;i++)legal.insert(ww.substr(i,10));
 int nc;std::cin>>nc;
 for(int c=0;c<nc;c++){
  long long x0,y0;int h0;std::string w;std::cin>>x0>>y0>>h0>>w;if(w=="-")w="";
  const long long vx[4]={0,1,0,-1},vy[4]={1,0,-1,0};
  long long x=x0,y=y0,dx=vx[h0],dy=vy[h0];
  std::map<Pt,bool> last;std::set<Pt> seed;bool feasible=true;
  for(char ch:w){bool bit=ch=='L';Pt p={x,y};auto it=last.find(p);
   if(it==last.end()){if(bit)seed.insert(p);}else if(it->second==bit){feasible=false;break;}
   last[p]=bit;long long ndx=bit?-dy:dy,ndy=bit?dx:-dx;dx=ndx;dy=ndy;x+=dx;y+=dy;
  }
  if(!feasible){std::cout<<"NO\n";continue;}
  auto black=seed;x=x0;y=y0;dx=vx[h0];dy=vy[h0];std::string hist;long long defects=0;
  for(char ch:w){Pt p={x,y};bool bit=black.count(p);if(bit!=(ch=='L'))return 2;
   hist+=ch;if(hist.size()==10){if(!legal.count(hist))defects++;hist.erase(0,1);}
   if(bit)black.erase(p);else black.insert(p);
   long long ndx=bit?-dy:dy,ndy=bit?dx:-dx;dx=ndx;dy=ndy;x+=dx;y+=dy;
  }
  std::cout<<"YES "<<seed.size()<<' '<<defects<<' '<<black.size()<<' '<<x<<' '<<y<<' '<<dx<<' '<<dy<<'\n';
  for(auto p:seed)std::cout<<p.first<<' '<<p.second<<'\n';
  for(auto p:black)std::cout<<p.first<<' '<<p.second<<'\n';
 }
 return 0;
}
