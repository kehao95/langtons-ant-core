// Finite complete word enumeration only. Resource exhaustion returns code 10.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
using namespace std;
string W="RRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRRRRLLLLRLR";
int K=9,N=150,side;uint64_t cap=20000000,nodes=0,leaves=0;bool complete=true;
array<int,1024> allowed{};int dx[4]={0,1,0,-1},dy[4]={1,0,-1,0};
int *last;string word;ofstream out;
void dfs(int t,int x,int y,int h,int suffix){
 if(++nodes>cap){complete=false;return;}
 if(t==N){++leaves;out<<word<<'\n';return;}
 int idx=(x+N+2)*side+y+N+2,old=last[idx];
 for(int bit=0;bit<2;bit++){
  if(old==bit)continue;
  int next=((suffix<<1)|bit)&((1<<K)-1);
  if(t>=K-1&&!allowed[next])continue;
  int nh=(h+(bit?-1:1)+4)%4;
  last[idx]=bit;word.push_back(bit?'L':'R');dfs(t+1,x+dx[nh],y+dy[nh],nh,next);word.pop_back();last[idx]=old;
  if(!complete)return;
 }
}
int main(int argc,char**argv){
 if(argc!=5){cerr<<"usage: enumerate K DEPTH NODE_CAP OUTPUT\n";return 2;}K=stoi(argv[1]);N=stoi(argv[2]);cap=stoull(argv[3]);out.open(argv[4]);
 if(K<1||K>10||N<K||N>1000||cap==0||!out)return 3;
 for(int i=0;i<104;i++){int v=0;for(int j=0;j<K;j++)v=(v<<1)|(W[(i+j)%104]=='L');allowed[v]=1;}
 side=2*N+5;last=new int[side*side];fill(last,last+side*side,-1);dfs(0,0,0,0,0);
 cout<<"{\"k\":"<<K<<",\"depth\":"<<N<<",\"nodes\":"<<nodes<<",\"words\":"<<leaves<<",\"complete\":"<<(complete?"true":"false")<<"}\n";
 delete[] last;return complete?0:10;
}
