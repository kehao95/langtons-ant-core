// Independent graph unfolding, Tarjan SCCs and complete integer rank audit.
// Inputs are the pinned previous theorem's full words and quotient witnesses.
// This checks the NEW finite lift, not the old all-parameter physical lemma.
#include <algorithm>
#include <array>
#include <fstream>
#include <functional>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>
using namespace std;
void require(bool yes,const string& text){if(!yes)throw runtime_error(text);}
int main(int argc,char**argv){try{
 require(argc==4||argc==5,"usage: verifier words quotient output-dir [candidate-ranks]");
 ifstream ws(argv[1]),qs(argv[2]);require(bool(ws)&&bool(qs),"missing base certificate");
 vector<string> words;set<string> vv;string line;map<string,int> phase;
 while(getline(ws,line)){require(line.size()==150&&line.find_first_not_of("LR")==string::npos,"invalid word");words.push_back(line);vv.insert(line.substr(0,149));vv.insert(line.substr(1));}
 require(words.size()==6605&&is_sorted(words.begin(),words.end())&&adjacent_find(words.begin(),words.end())==words.end(),"base word count/order");
 while(getline(qs,line)){istringstream ss(line);string word;int n;require(bool(ss>>word>>n),"invalid quotient row");require(word.size()==149&&n>=0&&n<102&&phase.emplace(word,n).second,"invalid quotient");}
 require(phase.size()==366&&vv.size()==6501,"base sizes");
 const string B="RRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRLL";
 map<pair<int,char>,int> model;for(int i=0;i<102;++i)model[{i,B[i]}]=(i+1)%102;model[{0,'L'}]=75;
 vector<string> base(vv.begin(),vv.end());map<string,vector<string>> adj;
 int quotient_edges=0;
 for(const auto&w:words){string v=w.substr(0,149),u=w.substr(1);adj[v].push_back(u);
  if(phase.count(v)&&phase.count(u)){++quotient_edges;auto it=model.find({phase[v],u.back()});require(it!=model.end()&&it->second==phase[u],"bad quotient edge");}}
 require(quotient_edges==370,"quotient edge coverage");
 vector<pair<string,int>> nodes;map<pair<string,int>,int> ids;
 for(const auto&v:base)for(int n=0;n<(phase.count(v)?4:1);++n){
  if(n==3&&phase.at(v)==0){continue;}
  ids[{v,n}]=int(nodes.size());nodes.push_back({v,n});}
 vector<vector<int>> graph(nodes.size());int edge_count=0;
 for(size_t a=0;a<nodes.size();++a){auto[v,n]=nodes[a];
  for(const auto&u:adj[v]){int m=0;if(phase.count(v)&&phase.count(u))m=n+(phase.at(v)==0&&u.back()=='R');
   if(phase.count(u)&&(m>3||(m==3&&phase.at(u)==0)))continue;
   graph[a].push_back(ids.at({u,m}));++edge_count;}
  sort(graph[a].begin(),graph[a].end());}
 require(nodes.size()==7595&&edge_count==7763,"lift coverage sizes");
 // Tarjan, unlike the Python verifier's two-pass SCC decomposition.
 int serial=0;vector<int> index(nodes.size(),-1),low(nodes.size()),stack,component(nodes.size(),-1);vector<bool> on(nodes.size());vector<vector<int>> comps;
 function<void(int)> visit=[&](int v){index[v]=low[v]=serial++;stack.push_back(v);on[v]=true;
  for(int u:graph[v]){if(index[u]<0){visit(u);low[v]=min(low[v],low[u]);}else if(on[u])low[v]=min(low[v],index[u]);}
  if(low[v]==index[v]){vector<int> c;for(;;){int u=stack.back();stack.pop_back();on[u]=false;component[u]=int(comps.size());c.push_back(u);if(u==v)break;}comps.push_back(c);}};
 for(int v=0;v<int(nodes.size());++v)if(index[v]<0)visit(v);
 vector<bool> cyclic(comps.size(),false);vector<int> periods;
 for(int i=0;i<int(comps.size());++i){cyclic[i]=comps[i].size()>1;
  for(int v:comps[i])for(int u:graph[v])if(u==v)cyclic[i]=true;
  if(cyclic[i]){periods.push_back(int(comps[i].size()));
   for(int v:comps[i]){int n=0;for(int u:graph[v])n+=component[u]==i;require(n==1,"not a simple cycle");}}}
 sort(periods.begin(),periods.end());require(periods==vector<int>({24,28,28,28,104}),"unexpected recurrent components");
 vector<set<int>> dag(comps.size());for(int v=0;v<int(nodes.size());++v)for(int u:graph[v])if(component[v]!=component[u])dag[component[v]].insert(component[u]);
 vector<array<int,3>> rank(comps.size(),array<int,3>{0,0,0});vector<int> done(comps.size(),0);
 function<void(int)> solve=[&](int i){require(done[i]!=1,"condensation cycle");if(done[i]==2)return;done[i]=1;array<int,3> tail{0,0,0};
  for(int j:dag[i]){solve(j);for(int k=0;k<3;++k)tail[k]=max(tail[k],rank[j][k]);}
  array<int,3> weights{int(cyclic[i]),int(!cyclic[i]),cyclic[i]?int(comps[i].size()):0};for(int k=0;k<3;++k)rank[i][k]=weights[k]+tail[k];done[i]=2;};
 for(int i=0;i<int(comps.size());++i)solve(i);
 vector<array<int,3>> h(nodes.size());for(int v=0;v<int(nodes.size());++v)h[v]=rank[component[v]];
 if(argc==5){ifstream input(argv[4]);require(bool(input),"missing supplied ranks");for(int v=0;v<int(nodes.size());++v){string word;int count;array<int,3> x;
  require(bool(input>>word>>count>>x[0]>>x[1]>>x[2]),"missing rank row");require(make_pair(word,count)==nodes[v],"rank node mismatch");h[v]=x;}
  string excess;require(!(input>>excess),"extra rank rows");}
 array<int,3> maximum{0,0,0};long long local_checks=0;
 for(int v=0;v<int(nodes.size());++v){int i=component[v];array<int,3> w{int(cyclic[i]),int(!cyclic[i]),cyclic[i]?int(comps[i].size()):0};
  for(int k=0;k<3;++k){require(h[v][k]>=w[k],"rank terminal/nonnegative condition");maximum[k]=max(maximum[k],h[v][k]);}
  for(int u:graph[v]){++local_checks;for(int k=0;k<3;++k){if(component[u]==i)require(h[v][k]==h[u][k],"cycle rank inconsistent");else require(h[v][k]>=w[k]+h[u][k],"rank edge inequality");}}}
 require(maximum==array<int,3>{5,956,212},"rank bound");
 ofstream es(string(argv[3])+"/cpp_edges.txt"),hs(string(argv[3])+"/cpp_ranks.txt");require(bool(es)&&bool(hs),"output unavailable");
 for(int v=0;v<int(nodes.size());++v){auto[word,n]=nodes[v];hs<<word<<'\t'<<n;for(int k=0;k<3;++k)hs<<'\t'<<h[v][k];hs<<'\n';
  for(int u:graph[v])es<<word<<'\t'<<n<<'\t'<<nodes[u].first<<'\t'<<nodes[u].second<<'\n';}
 cout<<"{\"status\":\"passed\",\"vertices\":"<<nodes.size()<<",\"edges\":"<<edge_count<<",\"all_edge_rank_checks\":"<<local_checks<<",\"periodic_plan_bound\":5,\"noncyclic_update_bound\":956,\"period_sum_bound\":212,\"HC_proved\":false}"<<endl;
 return 0;
}catch(const exception&e){cerr<<e.what()<<endl;return 1;}}
