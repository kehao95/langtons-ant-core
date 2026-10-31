// Finite literal controls only: no compressed formulas or prior simulator.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <unordered_set>
#include <vector>
using namespace std;
using I=long long;
uint64_t key(int x,int y){return(uint64_t(uint32_t(x))<<32)|uint32_t(y);}
pair<int,int> cell(uint64_t v){return{int32_t(v>>32),int32_t(v)};}
int main(int argc,char**argv){
 if(argc!=2)return 2;ifstream in(argv[1]);int cases;if(!(in>>cases)||cases<0)return 2;
 int dx[]={0,1,0,-1},dy[]={1,0,-1,0};
 for(int id=0;id<cases;id++){
  int l,r,count;in>>l>>r>>count;if(!in||l<0||r<0||l>10000||r>10000||count<0)return 2;
  vector<I>times(count);for(auto&t:times){in>>t;if(t<0||t>10000000)return 2;}
  if(!is_sorted(times.begin(),times.end()))return 2;
  vector<int>left{5,6,10,12,17};for(int j=0;j<l;j++){left.push_back(18);left.push_back(29);}
  vector<int>columns;for(auto i=left.rbegin();i!=left.rend();i++)columns.push_back(31-*i);
  for(int b:{6,10,12,17})columns.push_back(b);
  for(int j=0;j<r;j++){columns.push_back(18);columns.push_back(29);}
  unordered_set<uint64_t>black;for(int x=0;x<(int)columns.size();x++)for(int y=0;y<5;y++)
   if((columns[x]>>y)&1)black.insert(key(x,y));
  int x=2*l+5,y=3,h=1;I t=0;
  for(I target:times){
   while(t<target){auto p=key(x,y);if(black.erase(p))h=(h+3)%4;else{black.insert(p);h=(h+1)%4;}
    x+=dx[h];y+=dy[h];t++;}
   vector<pair<int,int>>full;for(auto v:black)full.push_back(cell(v));sort(full.begin(),full.end());
   cout<<id<<' '<<t<<' '<<x<<' '<<y<<' '<<h<<' '<<full.size();
   for(auto p:full)cout<<' '<<p.first<<' '<<p.second;cout<<'\n';
  }
 }
 return 0;
}
