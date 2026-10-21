// Independent finite-certificate checker, standard C++17 only.
// It does not trust the proposed composition table, graph edges, DP slopes,
// or the claimed numeric bounds. All are reconstructed from literal turns.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <queue>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>
using namespace std;
void require(bool ok,const string& s){if(!ok)throw runtime_error(s);}
const int NEG=-1000000000;
struct Reply{int channel,child;};
using Type=array<int,4>;
vector<Type> types[2][2];
vector<int> depth[2][2];
map<Type,int> typeid_[2][2];
int memo[2][2][16][269];
int inrow(int p,int j){return 2*j+(1-p);}
int outrow(int p,int j){return 2*j+p;}
int dx[4]={0,1,0,-1},dy[4]={1,0,-1,0};
struct Atom{int b,x,y,h,cost;};
Atom column(int b,int y,int h){
 int x=0,t=0;
 do{int black=(b>>y)&1;b^=1<<y;h=(h+(black?3:1))&3;x+=dx[h];y+=dy[h];++t;
    require(t<=2,"one-column axis bound");}while(x==0&&y>=0&&y<4);
 return {b,x,y,h,t};
}
int rank_type(int s,int p,int id,vector<int>&mark){
 require(id>=0&&id<(int)types[s][p].size(),"bad type id");
 if(mark[id]==2)return depth[s][p][id];
 require(mark[id]==0,"cyclic purported protocol");mark[id]=1;int r=0;
 for(int j=0;j<2;++j){int a=types[s][p][id][2*j],u=types[s][p][id][2*j+1];
  require((a==-1&&u==-1)||(a>=0&&a<2&&u>=0&&u<(int)types[s][p].size()),"bad response");
  if(a>=0)r=max(r,1+rank_type(s,p,u,mark));
 }
 mark[id]=2;return depth[s][p][id]=r;
}
int combine(int s,int p,int b,int r){
 int &cache=memo[s][p][b][r];if(cache>=0)return cache;
 require(cache!=-2,"nonterminating composition");cache=-2;
 Type row={-1,-1,-1,-1};
 for(int input=0;input<2;++input){int bb=b,rr=r,side=s,chan=input;
  while(true){Atom a=column(bb,inrow(p,chan),side==0?1:3);bb=a.b;
   if(a.x==0)break;
   int leaving=a.x>0?1:0,j=(a.y-p)/2;
   require(outrow(p,j)==a.y&&j>=0&&j<2,"wrong output parity");
   if(leaving==s){row[2*input]=j;row[2*input+1]=combine(s,p,bb,rr);break;}
   Type ans=types[s][1-p][rr];int next=ans[2*j+1];
   if(ans[2*j]<0)break;
   require(depth[s][1-p][next]<depth[s][1-p][rr],"child rank");
   chan=ans[2*j];rr=next;side=1-s;
  }
 }
 auto it=typeid_[s][p].find(row);require(it!=typeid_[s][p].end(),"catalog not closed");
 return cache=it->second;
}
struct Passage{int out,b,r,cost;string calls;};
Passage run_column_child(int p,int b,int r,int y,int h){
 int cost=0;string calls;
 while(true){Atom a=column(b,y,h);b=a.b;cost+=a.cost;
  if(a.x==0)return {-1,b,r,cost,calls};
  if(a.x<0)return {(a.y-p)/2,b,r,cost,calls};
  int j=(a.y-p)/2; // IN_(1-p) is OUT_p
  require(j>=0&&j<2&&inrow(1-p,j)==a.y,"child entry row");calls+=char('0'+j);
  Type ans=types[0][1-p][r];if(ans[2*j]<0)return {-1,b,r,cost,calls};
  y=outrow(1-p,ans[2*j]);r=ans[2*j+1];h=3;
 }
}
pair<int,string> script(int p,int b,int r,const string& seq){
 int cost=0;string calls;
 for(size_t i=0;i<seq.size();++i){int j=seq[i]-'0';require(j>=0&&j<2,"input bit");
  Passage a=run_column_child(p,b,r,inrow(p,j),1);b=a.b;r=a.r;cost+=a.cost;calls+=a.calls;
  require(a.out>=0||i+1==seq.size(),"script continues after terminal");
 }
 return {cost,calls};
}
int root_tag(int p,const Passage&a){return a.out<0?0:1+2*combine(0,p,a.b,a.r)+a.out;}
using Key=tuple<int,int,int,string>; // F=0,R=1; parity,type,request word
using Edge=array<int,5>; // target,weight,new mask,root y,root h
struct Rep{int kind,b,r,y,h,bb,rr,c;string calls;};
vector<pair<int,int>> ordinary[2][269];
vector<Rep> rooted[2][539];
void make_reps(){
 for(int p=0;p<2;++p)for(int b=0;b<16;++b){
  for(int r=0;r<269;++r){ordinary[p][combine(0,p,b,r)].push_back({b,r});
   for(int y=0;y<4;++y)for(int h=0;h<4;++h)if((h-p-y)%2==0){
    Passage a=run_column_child(p,b,r,y,h);
    rooted[p][root_tag(p,a)].push_back({0,b,r,y,h,a.b,a.r,a.cost,a.calls});
   }
  }
  for(int o=0;o<539;++o){Passage a;
   if(o==0)a={-1,b,0,0,""};else{int r=(o-1)/2,j=(o-1)%2;a=run_column_child(p,b,r,inrow(p,j),3);}
   rooted[p][root_tag(p,a)].push_back({1,b,o,-1,-1,a.b,a.r,a.cost,a.calls});
  }
 }
}
struct Literal{int time,x,y,h;vector<int>b,visits;};
Literal simulate(vector<int>b,int x,int y,int h){
 int n=b.size(),t=0;vector<int>visits(n,0);
 while(x>=0&&x<n&&y>=0&&y<4){
  require(t<10000000,"literal safety guard, UNKNOWN not proof");
  int c=(b[x]>>y)&1;b[x]^=1<<y;h=(h+(c?3:1))&3;++visits[x];x+=dx[h];y+=dy[h];++t;
 }
 return {t,x,y,h,b,visits};
}
int main(int argc,char**argv){try{
 require(argc==3,"usage: verify certificate.txt output-directory");ifstream f(argv[1]);require(bool(f),"missing certificate");
 string magic;f>>magic;require(magic=="FOUR_ROW_CERT_V1","bad certificate version");
 for(int s=0;s<2;++s)for(int p=0;p<2;++p){int ss,pp,n;f>>ss>>pp>>n;require(ss==s&&pp==p&&n==269,"catalog dimensions");
  types[s][p].resize(n);depth[s][p].assign(n,0);
  for(int i=0;i<n;++i){for(int&z:types[s][p][i])f>>z;require(typeid_[s][p].emplace(types[s][p][i],i).second,"duplicate behavior");}
  require(types[s][p][0]==Type{-1,-1,-1,-1},"bad empty block");vector<int>mark(n,0);
  for(int i=0;i<n;++i)rank_type(s,p,i,mark);
  require(*max_element(depth[s][p].begin(),depth[s][p].end())==13,"unexpected response depth");
 }
 for(auto &a:memo)for(auto &b:a)for(auto &c:b)fill(begin(c),end(c),-1);
 for(int s=0;s<2;++s)for(int p=0;p<2;++p)for(int b=0;b<16;++b)for(int r=0;r<269;++r)combine(s,p,b,r);
 const int expected[]={12,36,83,158,240,264,269,269};
 set<int> current[2][2];for(int s=0;s<2;++s)for(int p=0;p<2;++p)current[s][p].insert(0);
 for(int w=0;w<8;++w){set<int>next[2][2];
  for(int s=0;s<2;++s)for(int p=0;p<2;++p){for(int r:current[s][1-p])for(int b=0;b<16;++b)next[s][p].insert(combine(s,p,b,r));require((int)next[s][p].size()==expected[w],"width catalog count");}
  if(w==7)for(int s=0;s<2;++s)for(int p=0;p<2;++p)require(current[s][p]==next[s][p],"fixed point not closed");
  for(int s=0;s<2;++s)for(int p=0;p<2;++p)current[s][p]=next[s][p];
 }
 // Exact local-column bound, with both arbitrary persistent half-blocks.
 uint64_t cases=0;map<int,uint64_t>hist;int maximum=0;array<int,6>best{};
 for(int p=0;p<2;++p)for(int l=0;l<269;++l)for(int r=0;r<269;++r)for(int b=0;b<16;++b)
 for(int y=0;y<4;++y)for(int h=0;h<4;++h)if((h-p-y)%2==0){
  int bb=b,yy=y,hh=h,L=l,R=r,count=0;
  while(true){Atom a=column(bb,yy,hh);bb=a.b;count+=a.cost;if(a.x==0)break;
   int side=a.x>0?1:0,tag=1-side,i=(a.y-p)/2,id=side?R:L;
   Type ans=types[tag][1-p][id];if(ans[2*i]<0)break;
   if(side)R=ans[2*i+1];else L=ans[2*i+1];yy=outrow(1-p,ans[2*i]);hh=side?3:1;
  }
  ++cases;++hist[count];if(count>maximum){maximum=count;best={p,l,r,b,y,h};}
 }
 require(cases==18524416&&maximum==34,"column bound mismatch");
 uint64_t cutcases=0;int cutmax=0;array<int,5>cutbest{};
 for(int p=0;p<2;++p)for(int l=0;l<269;++l)for(int r=0;r<269;++r)for(int side=0;side<2;++side)for(int i=0;i<2;++i){
  int ids[2]={l,r},ss=side,j=i,count=1;
  while(true){Type a=types[1-ss][ss?1-p:p][ids[ss]];if(a[2*j]<0)break;ids[ss]=a[2*j+1];j=a[2*j];ss=1-ss;++count;}
  ++cutcases;if(count>cutmax){cutmax=count;cutbest={p,l,r,side,i};}
 }
 require(cutcases==578888&&cutmax==21,"cut crossing bound");
 // Verify every proposed max-plus graph edge against independently rebuilt
 // column additions, including BOTH possible locations of the initial root.
 int n,ne,ng;f>>n>>ne>>ng;require(n==21248&&ne==527764&&ng==1078,"graph sizes");
 vector<Key>states(n);map<Key,int>index;vector<vector<Edge>>graph(n);vector<int>goals(ng);
 for(int i=0;i<n;++i){int kind,p,t,len;string q;f>>kind>>p>>t>>len;
  require((kind==0||kind==1)&&(p==0||p==1)&&t>=0&&t<(kind?539:269)&&len<=14,"state format");
  for(int j=0;j<len;++j){int a;f>>a;require(a==0||a==1,"script alphabet");q+=char('0'+a);}
  states[i]={kind,p,t,q};require(index.emplace(states[i],i).second,"duplicate weighted state");
 }
 int readedges=0;for(int i=0;i<n;++i){int k;f>>k;require(k>=0&&k<100000,"bad edge count");graph[i].resize(k);readedges+=k;
  for(auto&e:graph[i]){for(int&z:e)f>>z;require(e[0]>=0&&e[0]<n&&e[1]>=0&&e[2]>=0&&e[2]<16,"edge format");}}
 require(readedges==ne,"edge total");for(int&g:goals)f>>g;require(bool(f),"truncated input");
 string extra;require(!(f>>extra),"unexpected input suffix");
 make_reps();
 auto locate=[&](int kind,int p,int t,string q){auto it=index.find({kind,p,t,q});require(it!=index.end(),"missing required weighted state");return it->second;};
 for(int v=0;v<n;++v){auto[kind,p,t,q]=states[v];vector<Edge>expected_edges;
  if(!kind){for(auto[b,r]:ordinary[p][t]){auto[c,sub]=script(p,b,r,q);expected_edges.push_back({locate(0,1-p,r,sub),c,b,-1,-1});}}
  else{require(t!=0||q.empty(),"terminal root script");
   for(const Rep&a:rooted[p][t]){auto[c,sub]=script(p,a.bb,a.rr,q);expected_edges.push_back({locate(a.kind,1-p,a.r,a.calls+sub),a.c+c,a.b,a.y,a.h});}}
  sort(expected_edges.begin(),expected_edges.end());auto supplied=graph[v];sort(supplied.begin(),supplied.end());
  require(expected_edges==supplied,"incomplete/incorrect recurrence edge list at "+to_string(v));
 }
 vector<int>goalcheck;for(int p=0;p<2;++p)for(int o=0;o<539;++o)goalcheck.push_back(locate(1,p,o,""));
 auto suppliedgoals=goals;sort(goalcheck.begin(),goalcheck.end());sort(suppliedgoals.begin(),suppliedgoals.end());require(goalcheck==suppliedgoals,"incomplete root goals");
 vector<char>seen(n,false);queue<int>queue_;for(int g:goals){seen[g]=1;queue_.push(g);}
 while(!queue_.empty()){int v=queue_.front();queue_.pop();for(auto e:graph[v])if(!seen[e[0]]){seen[e[0]]=1;queue_.push(e[0]);}}
 require(count(seen.begin(),seen.end(),true)==n,"unreachable weighted states");
 vector<vector<int>>V(24,vector<int>(n,NEG));
 for(int i=0;i<n;++i){auto[kind,p,t,q]=states[i];if(!kind&&t==0&&q.size()<=1)V[0][i]=0;}
 vector<int>maxima;
 for(int w=1;w<24;++w){for(int i=0;i<n;++i)for(auto e:graph[i])if(V[w-1][e[0]]!=NEG)V[w][i]=max(V[w][i],e[1]+V[w-1][e[0]]);
  int ans=NEG;for(int g:goals)ans=max(ans,V[w][g]);maxima.push_back(ans);}
 const vector<int>small={2,18,28,46,64,86,104,146,156,206,224,266};
 for(int i=0;i<12;++i)require(maxima[i]==small[i],"small exact maximum");
 for(int w=13;w<24;++w)require(maxima[w-1]==34*w-150,"pre-stability exact maximum");
 vector<int>A=V[20],B=V[21],DA(n),DB(n);for(int i=0;i<n;++i){require(A[i]!=NEG&&B[i]!=NEG,"finite stable support");DA[i]=V[22][i]-A[i];DB[i]=V[23][i]-B[i];}
 uint64_t inequalities=0;for(int i=0;i<n;++i){bool first=false,second=false;
  for(auto e:graph[i]){int u=e[0],w=e[1];
   require(B[i]>=w+A[u]&&A[i]+DA[i]>=w+B[u],"offset Bellman inequalities");
   require(DB[i]>=DA[u]&&DA[i]>=DB[u],"slope Bellman inequalities");inequalities+=4;
   if(B[i]==w+A[u]&&DB[i]==DA[u])first=true;
   if(A[i]+DA[i]==w+B[u]&&DA[i]==DB[u])second=true;
  }
  require(first&&second,"no tight growth-preserving edge");
 }
 bool attainA=false,attainB=false;for(int g:goals){require(A[g]<=530&&B[g]<=564&&DA[g]<=68&&DB[g]<=68,"goal affine envelope");attainA|=A[g]==530&&DA[g]==68;attainB|=B[g]==564&&DB[g]==68;}
 require(attainA&&attainB,"affine bound not attained");
 // Store all four checked integer vectors for a deterministic hash in Python.
 ofstream vectors(string(argv[2])+"/vectors.txt");for(int i=0;i<n;++i)vectors<<A[i]<<' '<<B[i]<<' '<<DA[i]<<' '<<DB[i]<<'\n';
 auto value=[&](int i,int w)->int64_t{if(w<24)return V[w][i];int base=(w%2)?21:20;return int64_t(base==20?A[i]:B[i])+int64_t((w-base)/2)*(base==20?DA[i]:DB[i]);};
 ofstream witnesses(string(argv[2])+"/witnesses.txt");vector<int>widths;for(int w=1;w<=23;++w)widths.push_back(w);for(int w:{40,41,200,201,1000,1001})widths.push_back(w);
 for(int w:widths){int g=goals[0];for(int x:goals)if(value(x,w)>value(g,w))g=x;int64_t answer=value(g,w);int startp=get<1>(states[g]);vector<int>masks;int rx=-1,ry=-1,rh=-1;
  for(int remain=w;remain>0;--remain){bool chosen=false;for(auto e:graph[g]){int u=e[0];if(value(u,remain-1)>NEG/2&&e[1]+value(u,remain-1)==value(g,remain)){
    masks.push_back(e[2]);if(e[3]>=0){require(rx<0,"multiple root births");rx=w-remain;ry=e[3];rh=e[4];}g=u;chosen=true;break;}}require(chosen,"missing witness edge");}
  require(value(g,0)==0&&rx>=0,"incomplete seed witness");Literal got=simulate(masks,rx,ry,rh);require(got.time==answer,"native seed witness replay");
  require((rh-rx-ry+10000)%2==startp,"root sector mismatch");
  witnesses<<w<<' '<<rx<<' '<<ry<<' '<<rh<<' '<<answer;for(int b:masks)witnesses<<' '<<b;witnesses<<'\n';
 }
 // Exhaustive ordinary dynamics, independent of every response abstraction.
 vector<int>brutemax;uint64_t bruteinputs=0,brutesteps=0;
 for(int w=1;w<=4;++w){int max_time=0;uint64_t limit=uint64_t(1)<<(4*w);
  for(uint64_t code=0;code<limit;++code){vector<int>b(w);for(int x=0;x<w;++x)b[x]=(code>>(4*x))&15;
   for(int x=0;x<w;++x)for(int y=0;y<4;++y)for(int h=0;h<4;++h){Literal a=simulate(b,x,y,h);max_time=max(max_time,a.time);++bruteinputs;brutesteps+=a.time;require(*max_element(a.visits.begin(),a.visits.end())<=34,"brute column overflow");}}
  require(max_time==small[w-1],"exhaustive root maximum");brutemax.push_back(max_time);
 }
 ofstream report(string(argv[2])+"/native.json");
 report<<"{\"status\":\"passed\",\"types_per_interface\":269,\"composition_cases\":17216,\"max_response_depth\":13,\"local_column_cases\":"<<cases<<",\"column_max\":"<<maximum<<",\"column_witness\":[";
 for(int i=0;i<6;++i)report<<(i?",":"")<<best[i];report<<"],\"cut_cases\":"<<cutcases<<",\"cut_max\":"<<cutmax<<",\"cut_witness\":[";
 for(int i=0;i<5;++i)report<<(i?",":"")<<cutbest[i];report<<"],\"weighted_states\":"<<n<<",\"weighted_edges\":"<<ne<<",\"root_goals\":"<<ng<<",\"stability_base\":20,\"stability_inequalities\":"<<inequalities<<",\"tight_edge_obligations\":"<<2*n<<",\"exact_small\":[";
 for(int i=0;i<12;++i)report<<(i?",":"")<<small[i];report<<"],\"brute_inputs\":"<<bruteinputs<<",\"brute_updates\":"<<brutesteps<<",\"native_maximizers\":"<<widths.size()<<",\"column_histogram\":{";
 bool sep=false;for(auto[k,v]:hist){report<<(sep?",":"")<<'"'<<k<<"\":"<<v;sep=true;}report<<"}}\n";
 cout<<"PASS: complete catalog, all recurrence edges, affine induction, literal controls\n";
}catch(const exception&e){cerr<<"REJECT: "<<e.what()<<'\n';return 1;}}
