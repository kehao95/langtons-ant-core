// Independent literal-word audit of PROOF.md Section 3. No screen.py code is used.
// Bounded endpoint words test conventions; they are not a theorem premise.
#include <algorithm>
#include <array>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>
using namespace std;
using Pt=pair<long long,long long>;
using Edge=tuple<Pt,Pt,int>;
long long floor_div(long long x,long long a){long long q=x/a,r=x%a;return q-(r<0);}
Pt canon(Pt p,Pt d){auto k=floor_div(p.first,d.first);return {p.first-k*d.first,p.second-k*d.second};}
int parity(long long x){return int((x%2+2)%2);}
unsigned long long kinematic_checks=0;
struct Result {bool valid=false;int K=0,F=0;Pt d;size_t ne=0;};
Result inspect(const string&w,int h){
 if(h<0||h>3||w.empty())throw runtime_error("bad word input");
 vector<Pt> pts;vector<int> dirs;
 Pt p={0,h%2},start=p;int heading=h;
 const array<Pt,4> moves={Pt{0,1},Pt{1,0},Pt{0,-1},Pt{-1,0}};
 for(char c:w){
  if(c!='R'&&c!='L')throw runtime_error("nonbinary word");
  pts.push_back(p);heading=(heading+(c=='R'?1:3))%4;dirs.push_back(heading);
  p.first+=moves[heading].first;p.second+=moves[heading].second;
 }
 Pt d={p.first-start.first,p.second-start.second};
 if(heading!=h||d.first==0||d.second==0)return {};
 if(d.first<0){
  d={-d.first,-d.second};p={-p.first,-p.second};
  for(auto&q:pts){q={-q.first,-q.second};}
  for(auto&v:dirs){v=(v+2)%4;}
 }
 const long long P=static_cast<long long>(w.size());
 map<Pt,int> D;map<Pt,vector<pair<long long,int>>> groups;map<Edge,int> edge_counts;
 for(int i=0;i<static_cast<int>(w.size());++i){
  Pt q=pts[i],s=canon(q,d),t=canon(i+1<static_cast<int>(w.size())?pts[i+1]:p,d);
  D[s]+=w[i]=='R'?1:-1;
  groups[s].push_back({i-P*floor_div(q.first,d.first),i});
  ++edge_counts[{s,t,dirs[i]}];
 }
 bool balanced=true;for(auto [q,c]:D)if(c!=0&&c!=1)balanced=false;
 int K=0;for(auto&[q,g]:groups){sort(g.begin(),g.end());for(int k=0;k<static_cast<int>(g.size());++k)if(w[g[k].second]=='L')K^=k%2;}
 vector<Edge> edges;for(auto&[e,c]:edge_counts)if(c%2)edges.push_back(e);
 auto key=[](const Edge&e,bool target){auto p=target?get<1>(e):get<0>(e);int h=get<2>(e);return tuple{p.second,p.first,int(h==0||h==1)};};
 int E=0;for(size_t i=0;i<edges.size();++i)for(size_t j=i+1;j<edges.size();++j)E^=(key(edges[i],false)<key(edges[j],false))!=(key(edges[i],true)<key(edges[j],true));
 map<Pt,int> positive_in,positive_out;
 for(auto e:edges)if(get<2>(e)==0||get<2>(e)==1){positive_out[get<0>(e)]^=1;positive_in[get<1>(e)]^=1;}
 int L_general=0;
 for(auto const&entry:groups){auto q=entry.first;auto n=entry.second.size();int pv=positive_in[q]^positive_out[q];
  L_general^=(pv*static_cast<int>((n-1)%2))^(parity(q.first+q.second)?static_cast<int>((n*(n-1)/2)%2):0);}
 if((K^E^L_general)!=1)throw runtime_error("general kinematic factorization failed");
 ++kinematic_checks;if(!balanced)return {};
 int L=0;for(auto [q,delta]:D){int pv=positive_in[q]^positive_out[q];L^=parity(q.first+q.second)?(delta*(pv+1))%2:(pv*(delta+1))%2;}
 int F=E^L;if((K^F)!=1)throw runtime_error("rank/port factorization failed");
 return {true,K,F,d,edges.size()};
}
void emit(const string&w,int h,const Result&r){
 cout<<"WORD "<<w.size()<<" "<<w<<" "<<h<<" "<<r.K<<" "<<r.F<<" "<<r.d.first<<" "<<r.d.second<<" "<<r.ne<<"\n";
}
int main(int argc,char**argv){
 try{
  if(argc==3&&string(argv[1])=="--exhaust"){
   int last=stoi(argv[2]);if(last<2||last>20||last%2)throw runtime_error("bounded audit supports even cap through 20");
   for(int n=2;n<=last;n+=2){
    unsigned long long valid=0,words=0,before=kinematic_checks;
    for(unsigned mask=0;mask<(1u<<n);++mask){
     string w(n,'R');for(int k=0;k<n;++k)if(mask&(1u<<k))w[k]='L';
     ++words;auto r=inspect(w,0);if(r.valid){++valid;emit(w,0,r);}
    }
    cout<<"COUNT "<<n<<" "<<words<<" "<<valid<<" "<<(kinematic_checks-before)<<"\n"<<flush;
   }
  }else if(argc==1){string w;int h;while(cin>>w>>h){auto r=inspect(w,h);if(!r.valid)throw runtime_error("control has invalid class balances");emit(w,h,r);}}
  else throw runtime_error("usage: audit [--exhaust EVEN_CAP]");
 }catch(const exception&e){cerr<<e.what()<<"\n";return 1;}
}
