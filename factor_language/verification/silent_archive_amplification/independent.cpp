// Independent literal controls only; the all-parameter proof is not inferred
// from these runs. Input is a transparent whitespace protocol from check.py.
#include <algorithm>
#include <array>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>
using P = std::pair<long long,long long>;
using Field = std::set<P>;
void need(bool p, const char* s) { if (!p) throw std::runtime_error(s); }
const std::array<P,4> dir{{{0,1},{1,0},{0,-1},{-1,0}}};
void toggle(Field& b, P q) { auto it=b.find(q); if(it==b.end()) b.insert(q); else b.erase(it); }
Field field() { long long m,x,y; std::cin>>m; need(m>=0,"bad field size"); Field b;
  while(m--) { std::cin>>x>>y; need(b.insert({x,y}).second,"duplicate field point"); } return b; }
std::string inverse9(Field b, P p, int h) {
  std::string s;
  for(int i=0;i<9;i++) { p.first-=dir[h].first; p.second-=dir[h].second; toggle(b,p);
    bool old=b.count(p); s.push_back(old?'L':'R'); h=(h+(old?1:3))%4; }
  std::reverse(s.begin(),s.end()); return s;
}
int main() {
  try {
    int cases; std::cin>>cases; need(cases>0,"empty controls");
    for(int trial=0;trial<cases;trial++) {
      long long n; std::cin>>n; need(n>=1 && n<=100000,"native n out of declared domain");
      Field b=field(), original=b;
      P p{-1,0}; int h=3; std::string W,past; std::cin>>W>>past;
      need(W.size()==104 && past.size()==9,"word lengths");
      need(inverse9(b,p,h)==past,"inverse past disagrees");
      std::set<std::string> legal;
      auto twice=W+W; for(int i=0;i<104;i++) legal.insert(twice.substr(i,10));
      int count; std::cin>>count; need(count==6,"block count");
      std::vector<std::pair<std::string,long long>> blocks;
      for(int i=0;i<count;i++) { std::string w; long long k; std::cin>>w>>k; blocks.push_back({w,k}); }
      std::vector<Field> targets; for(int i=0;i<3;i++) targets.push_back(field());
      std::map<P,long long> born; for(auto q:b) born[q]=-1;
      long long t=0,first=-1,pulse_bad=0,dead_initial=0,lifechecks=0,maxy=p.second;
      for(int block=0;block<6;block++) {
        const auto& w=blocks[block].first; auto copies=blocks[block].second;
        for(long long j=0;j<copies;j++) for(int i=0;i<(int)w.size();i++) {
          const bool black=b.count(p); const char a=black?'L':'R';
          need(a==w[i],"literal read disagrees with proposed word");
          std::string window=past+a;
          const bool bad=!legal.count(window);
          if(bad && first<0) { first=t; need(p==P(1,4) && h==1,"first defect pose"); }
          if(block<4) { need(!bad,"defect inside claimed legal prelude"); maxy=std::max(maxy,p.second); }
          if(block==4) {
            pulse_bad+=bad;
            if(i==1 || i==19) {
              need(black,"selected fuel must be black");
              auto birth=born.at(p);
              auto expect=i==1 ? 44+28*j : 56*n+146-28*j;
              need(birth==expect && birth>=0 && birth<56*n+167,"selected last-writer mismatch");
              if(i==1) need(bad,"left fuel must be J10");
              lifechecks++;
            }
          }
          if(black) { if(born.at(p)==-1) dead_initial++; born.erase(p); }
          else born[p]=t;
          toggle(b,p); h=(h+(black?3:1))%4;
          p.first+=dir[h].first; p.second+=dir[h].second;
          past=window.substr(1); t++;
        }
        if(block>=3) {
          need(b==targets[block-3],"complete checkpoint field mismatch");
          if(block==3) {
            need(dead_initial==(long long)original.size(),"unconsumed initial black lifetime");
            need(p==P(0,4) && h==0,"return pose");
          }
        }
      }
      need(first==56*n+168 && pulse_bad==9*n+6 && maxy==4*n+13,"summary formula");
      need(p==P(0,4*n+9) && h==3 && t==76*n+190,"final time/pose");
      need(lifechecks==2*(n+1),"lifetime coverage");
      std::cout<<n<<' '<<t<<' '<<first<<' '<<pulse_bad<<' '<<lifechecks<<' '<<b.size()<<' '<<maxy<<'\n';
    }
    need(bool(std::cin),"malformed input");
  } catch (const std::exception& e) { std::cerr<<e.what()<<'\n'; return 1; }
}
