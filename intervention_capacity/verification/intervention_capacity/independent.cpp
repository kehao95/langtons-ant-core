// Separate heading-index literal dynamics and full-drift chronology audit.
// No Python execution or prior project simulator is used.
#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>
using Point=std::pair<long long,long long>;
const long long DX[4]={0,1,0,-1}, DY[4]={1,0,-1,0};
struct Visit {long long time,index;char turn;};
long long floor2(long long x){return x>=0?x/2:-((-x+1)/2);}
int audit_period(const std::string& word,int start_h,const std::set<Point>& seed){
 long long x=0,y=0;int h=start_h;std::vector<Point> reads;
 for(char c:word){reads.push_back({x,y});h=(h+(c=='R'?1:3))%4;x+=DX[h];y+=DY[h];}
 if(x!=2 || (y!=2 && y!=-2) || h!=start_h)throw std::runtime_error("bad drift");
 std::map<Point,std::vector<Visit>> groups;
 for(size_t i=0;i<reads.size();++i){long long k=floor2(reads[i].first);
  Point key={reads[i].first-2*k,reads[i].second-y*k};
  groups[key].push_back({(long long)i-(long long)word.size()*k,k,word[i]});}
 std::set<Point> required;int comparisons=0;
 for(auto& [rep,events]:groups){
  std::set<long long> cutset;for(auto v:events)cutset.insert(v.index);
  std::vector<long long> cuts(cutset.begin(),cutset.end());
  for(size_t q=0;q<cuts.size();++q){std::vector<Visit> elig;
   for(auto v:events)if(v.index<=cuts[q])elig.push_back(v);
   std::sort(elig.begin(),elig.end(),[](Visit a,Visit b){return a.time<b.time;});
   for(size_t i=1;i<elig.size();++i){++comparisons;
    if(elig[i-1].turn==elig[i].turn)throw std::runtime_error("nonalternating");}
   if(q+1==cuts.size()){if(elig[0].turn!='R')throw std::runtime_error("infinite black ray");}
   else if(elig[0].turn=='L')for(long long j=cuts[q];j<cuts[q+1];++j)
    required.insert({rep.first+2*j,rep.second+y*j});
  }
 }
 if(required!=seed)throw std::runtime_error("complete seed mismatch");
 return comparisons;
}
int main(int argc,char**argv){try{
 if(argc!=2)throw std::runtime_error("input path required");
 std::ifstream in(argv[1]);std::string W;in>>W;
 for(int c=0;c<2;++c){int h,n;in>>h>>n;std::set<Point>B;
  for(int i=0;i<n;++i){long long x,y;in>>x>>y;B.insert({x,y});}
  std::cout<<"PERIOD "<<audit_period(W,h,B)<<'\n';}
 int cases;in>>cases;
 for(int id=0;id<cases;++id){long long steps,flip,x,y;int h,n;
  in>>steps>>flip>>x>>y>>h>>n;std::set<Point>B;
  for(int i=0;i<n;++i){long long a,b;in>>a>>b;B.insert({a,b});}
  std::string turns;turns.reserve((size_t)steps);
  for(long long t=0;t<steps;++t){Point p{x,y};if(t==flip){if(B.count(p))B.erase(p);else B.insert(p);}
   bool black=B.count(p);if(black)B.erase(p);else B.insert(p);
   turns.push_back(black?'L':'R');h=(h+(black?3:1))%4;x+=DX[h];y+=DY[h];}
  std::cout<<id<<' '<<x<<' '<<y<<' '<<h<<' '<<B.size()<<'\n';
  std::cout<<(turns.empty()?"-":turns)<<'\n';
  for(auto p:B){std::cout<<p.first<<' '<<p.second<<' ';}
  std::cout<<'\n';}
 if(!in)throw std::runtime_error("truncated input");
 return 0;
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}}
