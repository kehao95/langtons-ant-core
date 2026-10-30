// Independent complete-field literal simulator used only for scoped checks.
// Coordinate range in this native control is bounded by its generated input.
#include <algorithm>
#include <iostream>
#include <set>
#include <string>
#include <utility>
#include <vector>
using P=std::pair<long long,long long>;
int main(){
    int cases; if(!(std::cin>>cases)||cases<0) return 2;
    const P directions[]={{0,1},{1,0},{0,-1},{-1,0}};
    for(int c=0;c<cases;++c){
        int n,h,T; P p; std::cin>>n>>p.first>>p.second>>h>>T;
        if(n<0||h<0||h>3||T<0||T>200000) return 3;
        std::set<P> black;
        for(int j=0;j<n;++j){P q;std::cin>>q.first>>q.second;black.insert(q);}
        P v=directions[h]; std::vector<P> path={p}; std::string word;
        for(int t=0;t<T;++t){
            if(black.erase(p)) {v={-v.second,v.first};word.push_back('L');}
            else {black.insert(p);v={v.second,-v.first};word.push_back('R');}
            p={p.first+v.first,p.second+v.second};path.push_back(p);
        }
        int final_h=0;while(directions[final_h]!=v)++final_h;
        std::cout<<c<<' '<<p.first<<' '<<p.second<<' '<<final_h<<' '<<black.size()<<'\n';
        std::cout<<(word.empty()?"-":word)<<'\n';
        for(P q:black)std::cout<<q.first<<' '<<q.second<<' ';std::cout<<'\n';
        for(P q:path)std::cout<<q.first<<' '<<q.second<<' ';std::cout<<'\n';
    }
    return std::cin?0:4;
}
