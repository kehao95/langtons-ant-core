// Independently written vector-turn dynamics and all-epoch parity verifier.
// Only finite certificate test coordinates use int64; no huge-coordinate claim.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>
using I=std::int64_t;
using P=std::pair<I,I>;
struct Hash {std::size_t operator()(const P& p) const noexcept {
  auto mix=[](std::uint64_t z){z+=0x9e3779b97f4a7c15ULL;z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL;z=(z^(z>>27))*0x94d049bb133111ebULL;return z^(z>>31);};
  return mix(static_cast<std::uint64_t>(p.first))^(mix(static_cast<std::uint64_t>(p.second))<<1);
}};
using Field=std::unordered_set<P,Hash>;
const std::array<P,4> directions={P{0,1},P{1,0},P{0,-1},P{-1,0}};
const std::string standard="RRLLLLRLRRRRLRRRRLLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRR";
P rotated(P v,bool black){return black?P{-v.second,v.first}:P{v.second,-v.first};}
int heading(P v){for(int i=0;i<4;i++)if(v==directions[i])return i;throw std::runtime_error("invalid direction");}
bool scale(P a,P d,I& k){
 if(d.first){if(a.first%d.first)return false;k=a.first/d.first;return a.second==k*d.second;}
 if(a.first||!d.second||a.second%d.second)return false;k=a.second/d.second;return true;
}
bool permanent(const Field&B,P p,P v,const std::string&w){
 std::vector<P> q;P o=p,ov=v;
 for(char c:w){q.push_back(p);v=rotated(v,c=='L');p.first+=v.first;p.second+=v.second;}
 P d{p.first-o.first,p.second-o.second};if(v!=ov||d==P{0,0})return false;
 for(std::size_t i=0;i<q.size();i++){
  std::map<I,int> changes;changes[0]=0;
  for(std::size_t j=0;j<q.size();j++){
   I s;if(scale({q[j].first-q[i].first,q[j].second-q[i].second},d,s)&&(s>0||(s==0&&j<i)))changes[s]^=1;
  }
  for(const P&b:B){I k;if(scale({b.first-q[i].first,b.second-q[i].second},d,k)&&k>=0){changes[k]^=1;changes[k+1]^=1;}}
  int bit=0;for(auto [k,change]:changes){bit^=change;if(bit!=(w[i]=='L'))return false;}
 }
 return true;
}
int main(){
 try{
  std::ios::sync_with_stdio(false);std::cin.tie(nullptr);
  I n,m,hx,hy,cap;int h;
  while(std::cin>>n>>m>>hx>>hy>>h>>cap){
   if(n<=0||m<=0||n>2001||m>2001||h<0||h>3||cap<0||cap>10000000)throw std::runtime_error("unsupported finite control");
   Field B;for(I x=0;x<n;x++)for(I y=0;y<m;y++)B.insert({x,y});
   P p{hx,hy},v=directions[h];std::string w,last;I t=0,first=-1;
   for(;t<=cap;t++){
    if(t>=208&&t%104==0){
     last=w.substr(w.size()-104);
     if((standard+standard).find(last)!=std::string::npos&&w.compare(w.size()-208,104,last)==0&&permanent(B,p,v,last)){
      first=t;while(first>0&&w[static_cast<std::size_t>(first-1)]==last[static_cast<std::size_t>((first-1-t)%104+104)%104])first--;
      break;
     }
    }
    if(t==cap)break;
    bool black=B.find(p)!=B.end();if(black)B.erase(p);else B.insert(p);
    w+=black?'L':'R';v=rotated(v,black);p.first+=v.first;p.second+=v.second;
   }
   if(first<0)throw std::runtime_error("INCONCLUSIVE literal resource cap");
   std::vector<P> sorted(B.begin(),B.end());std::sort(sorted.begin(),sorted.end());
   std::cout<<"{\"n\":"<<n<<",\"m\":"<<m<<",\"head\":["<<hx<<','<<hy<<','<<h<<"],\"first\":"<<first<<",\"boundary\":"<<t<<",\"pose\":["<<p.first<<','<<p.second<<','<<heading(v)<<"],\"tail\":\""<<last<<"\",\"word\":\""<<w<<"\",\"field\":[";
   bool comma=false;for(P q:sorted){if(comma)std::cout<<',';comma=true;std::cout<<'['<<q.first<<','<<q.second<<']';}
   std::cout<<"]}\n"<<std::flush;
  }
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 2;}
}
