// Independent vector-turn literal simulator. No matching-kernel implementation.
#include <boost/multiprecision/cpp_int.hpp>
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <set>
#include <sstream>
#include <string>
#include <tuple>
#include <utility>
using Z=boost::multiprecision::cpp_int;
using P=std::pair<Z,Z>;
using E=std::tuple<Z,Z,int>;
const int DX[4]={0,1,0,-1}, DY[4]={1,0,-1,0};
int heading(int dx,int dy){for(int h=0;h<4;h++)if(DX[h]==dx&&DY[h]==dy)return h;throw 1;}
E literal_next(const std::set<P>& B,E e){
 Z x=std::get<0>(e),y=std::get<1>(e);int h=std::get<2>(e),dx=DX[h],dy=DY[h],xx,yy;
 if(B.count({x,y})){xx=-dy;yy=dx;}else{xx=dy;yy=-dx;}
 return {x+xx,y+yy,heading(xx,yy)};
}
uint64_t digest(uint64_t h,const std::string& s){for(unsigned char c:s){h^=c;h*=1099511628211ULL;}return h;}
int main(){
 std::ios::sync_with_stdio(false);std::cin.tie(nullptr);
 int cases;if(!(std::cin>>cases))return 2;
 for(int c=0;c<cases;c++){
  int m,h,cap;Z x,y;std::cin>>m>>x>>y>>h>>cap;std::set<P>B;
  for(int i=0;i<m;i++){Z a,b;std::cin>>a>>b;B.insert({a,b});}
  E root={x,y,h},e=root;std::set<E>C;
  do{if(!C.insert(e).second||C.size()>std::max(4,8*m))return 3;e=literal_next(B,e);}while(e!=root);
  e=root;int t=0;uint64_t hash=14695981039346656037ULL;
  while(C.count(e)){
   if(t>=cap){std::cout<<"INCONCLUSIVE\n";return 4;}
   Z a=std::get<0>(e),b=std::get<1>(e);int hh=std::get<2>(e);
   bool black=B.count({a,b});std::ostringstream text;text<<a<<","<<b<<","<<hh<<","<<(black?'L':'R')<<";";
   hash=digest(hash,text.str());E next=literal_next(B,e);
   if(black)B.erase({a,b});else B.insert({a,b});e=next;t++;
  }
  std::cout<<t<<" "<<std::get<0>(e)<<" "<<std::get<1>(e)<<" "<<std::get<2>(e)<<" "<<B.size()<<" "<<hash;
  for(const auto& p:B)std::cout<<" "<<p.first<<" "<<p.second;
  std::cout<<"\n";
 }
}
