// Independent mutable-colour DFS and integer edge audit. C++17, no Python.
#include <algorithm>
#include <array>
#include <deque>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>
using namespace std;
const string W="RRLLLLRLRRRRLRRRRLLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRR";
const int dx[4]={0,1,0,-1},dy[4]={1,0,-1,0};
set<string> allowed;
map<pair<int,int>,bool> colour;
vector<string> words;
vector<long long> levels(301);
string path,bestword;int best=0;
long long calls=0;
void require(bool q,const string&s){if(!q)throw runtime_error(s);}
int weight(char c){return c=='L'?29:-23;}
void dfs(int x,int y,int h,int score){
 ++calls;int n=int(path.size());++levels[n];
 if(n<300&&(score>best||(score==best&&make_pair(n,path)<make_pair(int(bestword.size()),bestword)))){best=score;bestword=path;}
 if(n==300){words.push_back(path);return;}
 pair<int,int>p{x,y};auto it=colour.find(p);bool known=it!=colour.end();bool old=known?it->second:false;
 for(char c:string("RL")){
  bool black=c=='L';if(known&&old!=black)continue;
  path.push_back(c);
  if(path.size()>=10&&!allowed.count(path.substr(path.size()-10))){path.pop_back();continue;}
  colour[p]=!black;int g=(h+(c=='R'?1:3))%4;
  dfs(x+dx[g],y+dy[g],g,score+weight(c));
  if(known)colour[p]=old;else colour.erase(p);
  path.pop_back();
 }
}
int main(int argc,char**argv){try{
 require(argc==2||argc==3,"supply output directory and optional potential file");string root=argv[1];
 for(int i=0;i<104;++i)allowed.insert((W+W).substr(i,10));
 dfs(0,0,0,0);sort(words.begin(),words.end());
 require(words.size()==29559&&adjacent_find(words.begin(),words.end())==words.end(),"word coverage count");
 require(best==322&&bestword.size()==90,"short bound");
 vector<string>nodes;for(const auto&w:words){nodes.push_back(w.substr(0,299));nodes.push_back(w.substr(1));}
 sort(nodes.begin(),nodes.end());nodes.erase(unique(nodes.begin(),nodes.end()),nodes.end());
 require(nodes.size()==29334,"vertex count");map<string,int>ids;
 for(size_t i=0;i<nodes.size();++i)ids[nodes[i]]=int(i);
 vector<tuple<int,int,int>>edges;vector<vector<pair<int,int>>>back(nodes.size());
 for(const auto&w:words){int a=ids.at(w.substr(0,299)),b=ids.at(w.substr(1)),c=weight(w.back());edges.emplace_back(a,b,c);back[b].push_back({a,c});}
 vector<int>h(nodes.size(),0);vector<bool>in(nodes.size(),true);deque<int>todo;
 for(int i=int(nodes.size())-1;i>=0;--i)todo.push_back(i);
 long long updates=0;
 while(!todo.empty()){
  int b=todo.front();todo.pop_front();in[b]=false;
  require(++updates<10000000,"resource cap, no conclusion");
  for(auto[a,c]:back[b])if(h[a]<h[b]+c){h[a]=h[b]+c;if(!in[a]){todo.push_back(a);in[a]=true;}}
 }
 // A supplied candidate is checked without regenerating or repairing its data.
 if(argc==3){
  ifstream supplied(argv[2]);require(bool(supplied),"missing supplied potential");
  vector<int>candidate;int value;while(supplied>>value)candidate.push_back(value);
  require(supplied.eof()&&candidate.size()==nodes.size(),"invalid supplied potential");
  h=move(candidate);
 }
 // Generator is separate from these complete local inequalities.
 for(auto[a,b,c]:edges)require(h[a]>=c+h[b],"edge inequality");
 int lm=-100000;
 for(size_t i=0;i<nodes.size();++i){require(h[i]>=0,"nonnegative potential");int s=0;for(char c:nodes[i])s+=weight(c);lm=max(lm,s+h[i]);}
 require(lm==284&&*max_element(h.begin(),h.end())==251,"long bound");
 ofstream eout(root+"/cpp_words.generated"),hout(root+"/cpp_potential.generated");
 require(bool(eout)&&bool(hout),"output unavailable");
 for(auto&w:words){eout<<w<<'\n';}
 for(auto v:h){hout<<v<<'\n';}
 cout<<"{\"status\":\"passed\",\"vertices\":"<<nodes.size()<<",\"edges\":"<<edges.size()<<",\"short_maximum\":"<<best<<",\"long_maximum\":"<<lm<<",\"short_witness\":\""<<bestword<<"\",\"dfs_calls\":"<<calls<<",\"potential_queue_removals\":"<<updates<<",\"HC_proved\":false}"<<endl;
 return 0;
}catch(const exception&e){cerr<<e.what()<<endl;return 1;}}
