#include <iostream>
#include <vector>
#include "chain_rank.hpp"
struct N{int t,r,k,next,prev,v;};
int main(){
 std::ios::sync_with_stdio(false);
 int n,cap;
 while(std::cin>>n>>cap){
  if(n<0||n>856)return 2;
  std::vector<N> v(n);
  for(auto& a:v)if(!(std::cin>>a.t>>a.r>>a.k>>a.next>>a.prev>>a.v))return 3;
  try{std::cout<<(consecutive_chain_ranks(v,cap)?1:0)<<'\n';}
  catch(const std::exception&){return 4;}
 }
}
