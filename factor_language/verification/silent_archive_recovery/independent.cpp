// Independent literal heading implementation and infinite-epoch tail check.
// Input is finite declarative words and complete source fields, never Python states.
#include <algorithm>
#include <array>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>
using P=std::pair<long long,long long>;
const std::array<P,4> dirs={P{0,1},P{1,0},P{0,-1},P{-1,0}};
const std::string standard="RRLLLLRLRRRRLRRRRLLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRR";
void need(bool b,const char* s){if(!b)throw std::runtime_error(s);}
void flip(std::set<P>& b,P p){auto i=b.find(p);if(i==b.end())b.insert(p);else b.erase(i);}
P add(P p,P d){return {p.first+d.first,p.second+d.second};}
P scale(P p,long long a){return {p.first*a,p.second*a};}
bool multiple(P p,P d,long long& k){
    if(d.first==0){if(p.first!=0||d.second==0||p.second%d.second)return false;k=p.second/d.second;return true;}
    if(p.first%d.first)return false;
    k=p.first/d.first;return p.second==k*d.second;
}
std::string past9(std::set<P> b,P p,int h){
    std::string s;
    for(int i=0;i<9;++i){p=add(p,scale(dirs[h],-1));flip(b,p);bool old=b.count(p);s+=old?'L':'R';h=(h+(old?1:3))%4;}
    std::reverse(s.begin(),s.end());return s;
}
void tail_check(const std::set<P>& b,P p,int h,const std::string& w){
    need(w.size()==104&&(standard+standard).find(w)!=std::string::npos,"not standard");
    std::vector<P> q;P v=p;int g=h;
    for(char c:w){q.push_back(v);g=(g+(c=='R'?1:3))%4;v=add(v,dirs[g]);}
    P d={v.first-p.first,v.second-p.second};need(g==h&&std::abs(d.first)==2&&std::abs(d.second)==2,"tail drift");
    for(int i=0;i<104;++i){
        std::vector<long long> changes;std::set<long long> epochs={0};
        for(int j=0;j<104;++j){long long z=0;P diff={q[j].first-q[i].first,q[j].second-q[i].second};
            if(multiple(diff,d,z)&&(z>0||(z==0&&j<i))){changes.push_back(z);epochs.insert(z);}}
        for(P x:b){long long k=0;P diff={x.first-q[i].first,x.second-q[i].second};
            if(multiple(diff,d,k)&&k>=0){epochs.insert(k);epochs.insert(k+1);}}
        epochs.insert(*epochs.rbegin()+1);
        for(long long k:epochs){bool bit=b.count(add(q[i],scale(d,k)));for(long long z:changes)if(z<=k)bit=!bit;
            need(bit==(w[i]=='L'),"infinite tail mismatch");}
    }
}
int main(){try{
    std::ios::sync_with_stdio(false);std::cin.tie(nullptr);
    int cases;std::cin>>cases;std::set<std::string> legal;
    for(int i=0;i<104;++i)legal.insert((standard+standard).substr(i,10));
    for(int ci=0;ci<cases;++ci){
        int n,m,bc;std::cin>>n>>m;std::set<P>b;
        for(int i=0;i<m;++i){long long x,y;std::cin>>x>>y;need(b.insert({x,y}).second,"duplicate input");}
        P p;int h;std::cin>>p.first>>p.second>>h>>bc;
        std::vector<std::pair<std::string,long long>> blocks;
        for(int i=0;i<bc;++i){std::string w;long long c;std::cin>>w>>c;need(c>=0,"negative count");blocks.push_back({w,c});}
        std::string tail;std::cin>>tail;need(bool(std::cin),"incomplete input");
        std::string past=past9(b,p,h);long long t=0,events=0,last=-1,first=-1;char previous='?';
        auto step=[&](char expected){bool bit=b.count(p);char ch=bit?'L':'R';need(ch==expected,"literal requested turn mismatch");
            std::string win=past+ch;bool bad=!legal.count(win);if(bad){++events;last=t;if(first<0)first=t;}
            past=win.substr(1);flip(b,p);h=(h+(bit?3:1))%4;p=add(p,dirs[h]);++t;previous=ch;};
        for(const auto& block:blocks)for(long long j=0;j<block.second;++j)for(char ch:block.first)step(ch);
        need(previous!=tail.back(),"first entry not minimal");tail_check(b,p,h,tail);
        const auto endpoint=b;P ep=p;int eh=h;long long et=t;
        for(int i=0;i<9;++i)step(tail[i]);
        std::cout<<n<<' '<<et<<' '<<events<<' '<<last<<' '<<endpoint.size()<<' '<<ep.first<<' '<<ep.second<<' '<<eh<<' '<<first<<'\n';
        for(P q:endpoint)std::cout<<q.first<<' '<<q.second<<'\n';
    }
    return 0;
}catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}}
