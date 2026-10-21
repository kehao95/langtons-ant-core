// Independent finite-word enumeration: assigned current colours and vector turns.
// This finite control is not the all-parameter three-fold proof.
#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>
using Point=std::pair<int,int>;
std::string W="RRLLLLRLRRRRLRRRRLLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRR";
bool legal[1024]{};
std::map<Point,int> colour;
std::string word;
std::vector<std::string> words;
unsigned long long counts[151]{};
void dfs(int depth, Point p, Point direction, int history) {
    ++counts[depth];
    if(depth==150){words.push_back(word);return;}
    auto it=colour.find(p);
    bool known=it!=colour.end();
    int old=known?it->second:0;
    for(int bit=0;bit<2;++bit){
        if(known && bit!=old)continue;
        int window=((history<<1)|bit)&1023;
        if(depth>=9 && !legal[window])continue;
        colour[p]=1-bit;
        Point nextdir=bit?Point{-direction.second,direction.first}:Point{direction.second,-direction.first};
        Point next={p.first+nextdir.first,p.second+nextdir.second};
        word.push_back(bit?'L':'R');
        dfs(depth+1,next,nextdir,window&511);
        word.pop_back();
        if(known)colour[p]=old;else colour.erase(p);
    }
}
int main(int argc,char**argv){
    if(argc!=3){std::cerr<<"word output and count output required\n";return 2;}
    if(W.size()!=104)return 3;
    for(int i=0;i<104;++i){int n=0;for(int j=0;j<10;++j)n=(n<<1)|(W[(i+j)%104]=='L');legal[n]=true;}
    dfs(0,{0,0},{0,1},0);
    std::sort(words.begin(),words.end());
    std::ofstream out(argv[1]);for(const auto&w:words)out<<w<<'\n';
    std::ofstream c(argv[2]);for(int i=0;i<=150;++i)c<<counts[i]<<'\n';
    if(!out || !c)return 4;
    std::cout<<words.size()<<" finite words\n";
}
