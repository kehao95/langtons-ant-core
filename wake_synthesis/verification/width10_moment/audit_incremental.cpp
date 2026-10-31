// Experimental exact ordered-event search. Every cap/resource boundary is explicit.
// Positive words need independent infinite verification; unfinished search is UNKNOWN.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <functional>
#include <fstream>
#include <filesystem>
#include <map>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;
struct FC {int m,ae,ao,o;};
vector<FC> counts(int t,int I,int J,int cap,int odd=-1){vector<FC>v;for(int o=0;o<=1;o++)if(odd<0||o==odd)for(int a=0;a<=I;a++){
 int m=(t%2==0)?2*(I+J-2*a)+o:2*(J-I+2*a)-o;
 if(m>=0&&m<=cap/4&&a<=(m+1)/2&&I-a>=0&&I-a<=m/2)v.push_back({m,a,I-a,o});}
 sort(v.begin(),v.end(),[](auto a,auto b){return a.m<b.m;});return v;}
uint64_t key(array<int,4>x,int g,int dx){uint64_t k=0;for(int i=0;i<4;i++)k|=uint64_t(x[i])<<(8*i);return k|(uint64_t(g)<<32)|(uint64_t(dx+128)<<40);}
array<int,6> dec(uint64_t k){return{int(k&255),int((k>>8)&255),int((k>>16)&255),int((k>>24)&255),int((k>>32)&255),int((k>>40)&255)-128};}
array<int,4> transform(array<int,4>x,int row){return row%2?array<int,4>{x[2],x[3],x[1],x[0]}:array<int,4>{x[3],x[2],x[0],x[1]};}
int cap=104,target_growth=0;double time_cap=30;uint64_t node_cap=1000000000ULL;
array<unordered_map<uint64_t,int>,11>tables;
const bool standard_odd[11][2]={{1,1},{0,1},{0,1},{1,0},{1,0},{1,0},{0,1},{0,0},{1,0},{0,1},{1,1}};
bool pinned=false;
int wake_a=-1,wake_b=-1;
bool fixed_wake(){return wake_a>=0||pinned;}
int odd_at(int t,int r){return wake_a>=0?(((r?wake_b:wake_a)>>(t+10))&1):int(standard_odd[t+10][r]);}
string cache_dir;
bool tables_only=false;
void build_costs(){
 unordered_map<uint64_t,int>states;
 for(auto a:vector<array<int,2>>{{1,0},{0,1},{1,1}}){
  if(fixed_wake()&&a!=array<int,2>{odd_at(-10,0),odd_at(-10,1)})continue;
  array<int,4>f={a[0],a[1],a[0],a[1]};int z=a[0]+a[1];states[key(f,z,0)]=z;
  tables[1][key(transform(f,-10),z,0)]=z;
 }
 for(int t=-9;t<=-1;t++){
  unordered_map<uint64_t,int>next;
  string cache=cache_dir+"/layer"+to_string(t)+".bin";ifstream prior;if(wake_a<0)prior.open(cache,ios::binary);
  if(prior.is_open()){uint64_t n=0;prior.read((char*)&n,sizeof(n));for(uint64_t i=0;i<n;i++){uint64_t k;int c;prior.read((char*)&k,8);prior.read((char*)&c,4);next.emplace(k,c);}if(!prior)throw runtime_error("truncated cache");}
  else {
  for(auto[k,old]:states){auto s=dec(k);int I0=t%2?s[0]:s[1],I1=t%2?s[1]:s[0],J0=t%2?s[3]:s[2],J1=t%2?s[2]:s[3];
   auto v=counts(t,I0,J0,cap,fixed_wake()?odd_at(t,0):-1),w=counts(t,I1,J1,cap,fixed_wake()?odd_at(t,1):-1);
   for(auto a:v)for(auto b:w){int cost=old+a.m+b.m,g=s[4]+a.o+b.o,dx=s[5]+(t%2?(a.m+b.m-2*(J0+J1)):0);
    array<int,4>f={a.m-J0,b.m-J1,a.m-I0,b.m-I1};
    if(cost>cap-1||g>(target_growth?target_growth:16)||*min_element(f.begin(),f.end())<0||f[0]+f[1]==0)continue;
    auto kk=key(f,g,dx);auto it=next.find(kk);if(it==next.end()||cost<it->second)next[kk]=cost;
   }
  }
  if(wake_a<0){ofstream file(cache+".tmp",ios::binary);uint64_t n=next.size();file.write((char*)&n,8);for(auto[k,c]:next){file.write((char*)&k,8);file.write((char*)&c,4);}if(!file)throw runtime_error("cache save failed");}
  if(wake_a<0)filesystem::rename(cache+".tmp",cache);
  }
  states=move(next);
  for(auto[k,c]:states){auto s=dec(k);array<int,4>f={s[0],s[1],s[2],s[3]};tables[t+11][key(transform(f,t),s[4],s[5])]=c;}
  if(wake_a<0)cerr<<"cost layer "<<t<<" states "<<states.size()<<'\n';
 }
}
struct Node {int t,r,k,a,down,h,next=-1,prev=-1,v=0;size_t checkpoint=0,meta_checkpoint=0;};
using Row=array<vector<int>,2>;
struct E {int a,b;int64_t w;};
struct Limit:exception{string why;Limit(string x):why(x){}};

struct DifferenceSystem {
 struct Arc{int to;int64_t w;};struct Undo{int type,a,b;int64_t old;};
 array<vector<Arc>,256> adj;array<int64_t,256> potential{};vector<Undo>undo;
 size_t mark()const{return undo.size();}
 void rollback(size_t to){while(undo.size()>to){auto z=undo.back();undo.pop_back();if(z.type==0)adj[z.a].pop_back();else if(z.type==1)potential[z.a]=z.old;else adj[z.a][z.b].w=z.old;}}
 void set_potential(int v,int64_t w){undo.push_back({1,v,0,potential[v]});potential[v]=w;}
 bool propagate(int source,int target,int64_t w){
  if(potential[target]>=potential[source]+w)return true;
  if(source==target)return false;
  int queue[256],head=0,tail=0,count=0;bool queued[256]={};
  set_potential(target,potential[source]+w);queue[tail++]=target;tail%=256;count++;queued[target]=true;
  while(count){int v=queue[head++];head%=256;count--;queued[v]=false;
   for(auto e:adj[v])if(potential[e.to]<potential[v]+e.w){
    if(e.to==source)return false;
    set_potential(e.to,potential[v]+e.w);
    if(!queued[e.to]){queue[tail++]=e.to;tail%=256;count++;queued[e.to]=true;}
   }
  }return true;
 }
 bool add(int a,int b,int64_t w,int*slot=nullptr){int k=adj[a].size();if(slot)*slot=k;undo.push_back({0,a,k,0});adj[a].push_back({b,w});return propagate(a,b,w);}
 bool strengthen(int a,int slot,int64_t w){auto e=adj[a][slot];if(w<=e.w)return true;undo.push_back({2,a,slot,e.w});adj[a][slot].w=w;return propagate(a,e.to,w);}
} difference;
int rank_slot[256];
int component[256],position_in[256],component_size[256],phase_population[4]={};
struct MetaUndo{int i,root,pos,len;};vector<MetaUndo> meta_undo;
void restore_metadata(size_t mark){while(meta_undo.size()>mark){auto m=meta_undo.back();meta_undo.pop_back();component[m.i]=m.root;position_in[m.i]=m.pos;component_size[m.i]=m.len;}}

vector<Node>ns;uint64_t prefixes=0,badorder=0,badcycle=0,badbudget=0,leaf=0,stamp=0;
vector<int>seenrank;vector<uint64_t>seenstamp;array<uint64_t,11>layers{};int growth=0,dxsum=0;vector<string>solutions;
auto start=chrono::steady_clock::now();
void attach(int i,int j,int v){if(i<0||j<0||ns[i].next!=-1||ns[j].prev!=-1)throw runtime_error("invalid attach");ns[i].next=j;ns[i].v=v;ns[j].prev=i;}
int append(int t,int r,int k,int a,int lowerout,int lowerin,int vi,int vo){int dn=(t%2==0)?(a^(k%2)):!(a^(k%2));int pa=1-a,pd=1-dn;
 int h=t%2==0?(pa?1:3):(pa?0:2),i=ns.size();ns.push_back({t,r,k,pa,pd,h});ns.back().checkpoint=difference.mark();ns.back().meta_checkpoint=meta_undo.size();
 component[i]=i;position_in[i]=0;component_size[i]=1;phase_population[2*r+(t%2+2)%2]++;
 growth+=(k%2?-1:1);if(t%2)dxsum+=pd?-1:1;
 if(a)attach(lowerout,i,vi);if(dn)attach(i,lowerin,vo);return i;}
void pop(){auto nd=ns.back();difference.rollback(nd.checkpoint);restore_metadata(nd.meta_checkpoint);phase_population[2*nd.r+(nd.t%2+2)%2]--;int i=ns.size()-1;if(nd.prev>=0){ns[nd.prev].next=-1;ns[nd.prev].v=0;}if(nd.next>=0)ns[nd.next].prev=-1;
 growth-=(nd.k%2?-1:1);if(nd.t%2)dxsum-=nd.down?-1:1;ns.pop_back();}
int lower_cost(int t,array<int,4>f,int gp,int xp){int best=cap+1;if(*min_element(f.begin(),f.end())<0)return best;
 for(int g:{8,12,16}){if(target_growth&&target_growth!=g)continue;int need=g-gp,dx=2-xp;if(need<0||need>16||dx<-128||dx>127)continue;
 auto it=tables[t+10].find(key(f,need,dx));if(it!=tables[t+10].end())best=min(best,it->second);}
 return best;}
void tick(){prefixes++;if(prefixes>node_cap)throw Limit("UNKNOWN_NODE_CAP");if((prefixes&1023)==0&&chrono::duration<double>(chrono::steady_clock::now()-start).count()>time_cap)throw Limit("UNKNOWN_TIME_CAP");}
bool feasible(){
 const int n=ns.size(),last=n-1;
 if((*max_element(phase_population,phase_population+4))*4>cap){badorder++;return false;}
 int p=ns[last].prev,q=ns[last].next;
 if(p>=0){int64_t w=1-int64_t(cap)*ns[p].v;if(!difference.add(p,last,w)||!difference.add(last,p,-w)){badorder++;return false;}}
 if(q>=0){int64_t w=1-int64_t(cap)*ns[last].v;if(!difference.add(last,q,w)||!difference.add(q,last,-w)){badorder++;return false;}}
 if(ns[last].k&& !difference.add(last-1,last,4,&rank_slot[last])){badorder++;return false;}
 int start=last,back=0;
 while(ns[start].prev>=0){start=ns[start].prev;if(++back>=n){badcycle++;return false;}}
 int members[256],length=0,voltage=0;int current=start;++stamp;
 while(current>=0){
  members[length++]=current;
  int coordinate=ns[current].r+2*voltage;
  int ix=(ns[current].t+10)*(4*cap+3)+coordinate+2*cap;
  if(ix<0||ix>=int(seenrank.size()))throw runtime_error("coordinate stamp overflow");
  if(seenstamp[ix]==stamp&&seenrank[ix]+1!=ns[current].k){badorder++;return false;}
  seenstamp[ix]=stamp;seenrank[ix]=ns[current].k;
  voltage+=ns[current].v;current=ns[current].next;
 }
 for(int k=0;k<length;k++){
  int i=members[k];meta_undo.push_back({i,component[i],position_in[i],component_size[i]});
  component[i]=start;position_in[i]=k;component_size[i]=length;
 }
 int ranks[256],nr=0;bool touched[256]={};
 for(int k=0;k<length;k++){
  int i=members[k];
  if(ns[i].k&&!touched[i]){touched[i]=true;ranks[nr++]=i;}
  if(i+1<n&&ns[i+1].t==ns[i].t&&ns[i+1].r==ns[i].r&&ns[i+1].k==ns[i].k+1&&!touched[i+1]){touched[i+1]=true;ranks[nr++]=i+1;}
 }
 for(int k=0;k<nr;k++){
  int i=ranks[k],j=i-1;
  if(j<0||ns[j].t!=ns[i].t||ns[j].r!=ns[i].r||ns[j].k+1!=ns[i].k)throw runtime_error("rank order");
  if(component[j]!=component[i]){int w=max(4,component_size[j]+position_in[i]-position_in[j]);w=(w+3)/4*4;
   if(!difference.strengthen(j,rank_slot[i],w)){badorder++;return false;}
  }
 }
 return true;
}

// Reference feasibility constructed from scratch after every sampled appended
// prefix. This oracle intentionally does not share DifferenceSystem data.
long long audit_remaining=100000;
bool reference_feasible() {
 int n=ns.size();
 int phases[4]{};
 for(const Node &v:ns) phases[2*v.r+(v.t%2+2)%2]++;
 if(4*(*max_element(phases,phases+4))>cap)return false;
 vector<int> root(n,-1), pos(n,-1),volt(n,-1),len(n,0);
 int nr=0;
 for(int i=0;i<n;i++) if(ns[i].prev<0) {
  int x=i,j=0,w=0;
  while(x>=0){ if(root[x]>=0)return false;
    root[x]=nr;pos[x]=j;volt[x]=w;
    w+=ns[x].v; x=ns[x].next; j++;
    if(j>n)return false;
  }
  len[nr++]=j;
 }
 for(int i=0;i<n;i++)if(root[i]<0)return false;
 vector<tuple<int,int,long long>> ed;
 for(int i=0;i<n;i++)if(ns[i].k>0){
  int j=i-1; if(j<0||ns[i].t!=ns[j].t||ns[i].r!=ns[j].r||ns[i].k!=ns[j].k+1)abort();
  long long value=(root[j]==root[i] ? 4+pos[j]-pos[i] : max(4+pos[j]-pos[i],len[root[j]]))+int64_t(volt[i]-volt[j])*cap;
  if(root[j]==root[i]){
    // In one chain the chronology constraint is exact: no free root offset.
    if(value>0) return false;
  } else ed.emplace_back(root[j],root[i],value);
 }
 // Use an entirely independent pairwise chain scan for same-cell skipped-rank.
 for(int r=0;r<nr;r++){
  vector<int> order;
  for(int i=0;i<n;i++)if(root[i]==r)order.push_back(i);
  sort(order.begin(),order.end(),[&](int i,int j){return pos[i]<pos[j];});
  map<pair<int,int>,int> last;
  for(int i:order){auto key=make_pair(ns[i].t,ns[i].r+2*volt[i]);
   auto it=last.find(key);
   if(it!=last.end()&&it->second+1!=ns[i].k)return false;
   last[key]=ns[i].k;
  }
 }
 vector<long long>dist(nr,0);
 for(int pass=0;pass<nr;pass++){
  bool changed=false;
  for(auto [i,j,w]:ed)if(dist[j]<dist[i]+w){dist[j]=dist[i]+w;changed=true;}
  if(!changed)return true;
 }
 return false;
}
void finish(){int P=ns.size(),i=0,n=0,v=0;vector<int>seen(P),tau(P);string w;
 if(P>cap||P%4||dxsum!=2||(growth!=8&&growth!=12&&growth!=16)||(target_growth&&growth!=target_growth))return;
 while(i>=0&&!seen[i]){seen[i]=1;tau[i]=n-P*v;w+=ns[i].k%2?'L':'R';n++;v+=ns[i].v;i=ns[i].next;}
 if(i!=0||n!=P||v!=1)return;for(int j=0;j<P;j++)if(ns[j].k&&tau[j]<=tau[j-1])return;
 leaf++;solutions.push_back(w);cout<<"SOLUTION "<<P<<' '<<growth<<' '<<w<<endl;
}
void rec(int t,const Row&old){layers[t+10]++;
 array<vector<int>,2>outs,ins;array<int,2>I,J,vi,vo;
 for(int r=0;r<2;r++){int sl=t%2?r:1-r;for(int i:old[sl])if(ns[i].down)outs[r].push_back(i);vi[r]=t%2?0:-int(sl==0);
 sl=t%2?1-r:r;for(int i:old[sl])if(ns[i].a)ins[r].push_back(i);vo[r]=t%2?int(r==1):0;I[r]=outs[r].size();J[r]=ins[r].size();}
 if(t==-10){if(I!=J||I[0]>1||I[1]>1||I[0]+I[1]==0)return;
  if(fixed_wake()&&I!=array<int,2>{odd_at(-10,0),odd_at(-10,1)})return;
  for(int r=0;r<2;r++)if(I[r])append(t,r,0,1,outs[r][0],ins[r][0],vi[r],vo[r]);
  finish();for(int r=1;r>=0;r--)if(I[r])pop();return;
 }
 array<vector<FC>,2>finals;for(int r=0;r<2;r++)finals[r]=counts(t,I[r],J[r],cap,fixed_wake()?odd_at(t,r):-1);
 map<int,vector<FC>>pairs;
 for(auto f:finals[0])for(auto g:finals[1]){int gp=growth+f.o+g.o,xp=dxsum+(t%2?2*(J[0]+J[1])-f.m-g.m:0);
  array<int,4>b={f.m-J[0],g.m-J[1],f.m-I[0],g.m-I[1]};int lower=lower_cost(t,b,gp,xp);
  if(int(ns.size())+f.m+g.m+lower<=cap)pairs[f.m].push_back(g);}
 if(pairs.empty()){badbudget++;return;}
 Row row;function<void(int,FC,int,int,int,int,int)>fill;
 fill=[&](int r,FC f,int k,int ni,int nj,int ae,int ao){tick();if(k==f.m){
   if(ni!=I[r]||nj!=J[r]||ae||ao)throw runtime_error("count endpoint");
   if(r==0)for(auto s:pairs[f.m])fill(1,s,0,0,0,s.ae,s.ao);else rec(t-1,row);return;}
  for(int bit=0;bit<2;bit++){int dn=t%2==0?(bit^(k%2)):!(bit^(k%2));if(ni+bit>I[r]||nj+dn>J[r])continue;
   int be=ae-(bit&&k%2==0),bo=ao-(bit&&k%2==1),kp=k+1;
   if(be<0||bo<0||be>(f.m+1)/2-(kp+1)/2||bo>f.m/2-kp/2)continue;
   int i=append(t,r,k,bit,bit?outs[r][ni]:-1,dn?ins[r][nj]:-1,vi[r],vo[r]);row[r].push_back(i);
   bool fast=feasible();
   if(audit_remaining>0){bool slow=reference_feasible();--audit_remaining;
      if(slow!=fast){cerr<<"MISMATCH n="<<ns.size()<<" fast="<<fast<<" slow="<<slow<<"\n";
         for(auto v:ns)cerr<<"NODE "<<v.t<<" "<<v.r<<" "<<v.k<<" "<<v.prev<<" "<<v.next<<" "<<v.v<<"\n";
         abort();}}
   if(fast)fill(r,f,kp,ni+bit,nj+dn,be,bo);
   row[r].pop_back();pop();}
 };
 for(auto f:finals[0])if(pairs.count(f.m))fill(0,f,0,0,0,f.ae,f.ao);
}
int main(int ac,char**av){if(ac>1)cap=stoi(av[1]);if(ac>2)target_growth=stoi(av[2]);if(ac>3)time_cap=stod(av[3]);if(ac>4)pinned=stoi(av[4]);
 if(cap<4||cap>244||cap%4||!(target_growth==0||target_growth==8||target_growth==12||target_growth==16))throw runtime_error("invalid parameters");
 cache_dir=(filesystem::temp_directory_path()/("hc-width10-"+to_string(cap)+"-"+to_string(target_growth)+"-"+to_string(pinned))).string();filesystem::create_directories(cache_dir);
 if(ac>5)tables_only=stoi(av[5]);
 if(ac>8)node_cap=stoull(av[8]);
 if(ac>7){wake_a=stoi(av[6]);wake_b=stoi(av[7]);if(!(wake_a&(1<<10)))throw runtime_error("missing normalized top");}
 seenrank.resize(11*(4*cap+3));seenstamp.resize(seenrank.size());build_costs();if(tables_only){cout<<"TABLES_DONE\n";return 0;}cerr<<"SEARCH_START\n";start=chrono::steady_clock::now();string status="COMPLETE";
 try{for(int second=0;second<=1;second++){if(fixed_wake()&&second!=odd_at(0,1))continue;Row top;top[0].push_back(append(0,0,0,0,-1,-1,0,0));if(second)top[1].push_back(append(0,1,0,0,-1,-1,0,0));
  if(int(ns.size())+lower_cost(0,{1,second,1,second},growth,0)<=cap)rec(-1,top);if(second)pop();pop();}}
 catch(Limit&e){status=e.why;}
 cout<<"{\"status\":\""<<status<<"\",\"cap\":"<<cap<<",\"growth\":"<<target_growth<<",\"pinned_wake\":"<<pinned<<",\"prefixes\":"<<prefixes<<",\"solutions\":"<<solutions.size()<<",\"order_rejections\":"<<badorder<<",\"cycle_rejections\":"<<badcycle<<",\"budget_rejections\":"<<badbudget<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<",\"layers\":[";
 for(int i=0;i<11;i++)cout<<(i?",":"")<<layers[i];cout<<"]}\n";
 return 0;
}
