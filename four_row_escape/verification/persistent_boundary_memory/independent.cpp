// Independent literal column and complete-rectangle verifier. C++17 only.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <vector>
using namespace std;
void demand(bool x,const char* why){if(!x)throw runtime_error(why);}
struct Node {int rank; vector<pair<int,int>> reply;};
const int dx[4]={0,1,0,-1},dy[4]={1,0,-1,0};
// White and black turns are explicit, separate from the Python vector rotation.
const int turn[2][4]={{1,2,3,0},{3,0,1,2}};
void column(int H,int& mask,int& x,int& y,int& h){
 x=0;int steps=0;
 do {int b=(mask>>y)&1;mask^=1<<y;h=turn[b][h];x+=dx[h];y+=dy[h];steps++;}
 while(x==0&&y>=0&&y<H);
 demand(steps<=2,"column exceeded two steps");
}
void check_catalogs(const char* name){
 ifstream f(name); demand(bool(f),"cannot read catalog certificate");
 int groups;f>>groups;long long equations=0,trees=0;
 for(int g=0;g<groups;g++){
  int H,n[2];f>>H>>n[0]>>n[1];demand(H>=1&&H<=4,"height");
  vector<int> in[2],out[2];vector<Node> nodes[2];
  vector<vector<int>> product[2];
  for(int p=0;p<2;p++)for(int y=0;y<H;y++){
   if(((y+p)&1)==1)in[p].push_back(y);else out[p].push_back(y);
  }
  for(int p=0;p<2;p++)for(int i=0;i<n[p];i++){
   Node a;f>>a.rank;int d=0;
   for(int j=0;j<(int)in[p].size();j++){
    int o,c;f>>o>>c;
    if(o<0)demand(c==-1,"terminal child");
    else{demand(o<(int)out[p].size()&&c>=0&&c<i,"tree order");d=max(d,1+nodes[p][c].rank);}
    a.reply.push_back({o,c});
   }
   demand(d==a.rank,"rank equality");nodes[p].push_back(a);trees++;
  }
  for(int p=0;p<2;p++){
   product[p].resize(1<<H,vector<int>(n[1-p]));
   for(auto& row:product[p])for(int& t:row){f>>t;demand(t>=0&&t<n[p],"product index");}
  }
  for(int p=0;p<2;p++)for(int b0=0;b0<(1<<H);b0++)for(int r0=0;r0<n[1-p];r0++){
   const Node parent=nodes[p][product[p][b0][r0]];
   for(int c=0;c<(int)in[p].size();c++){
    int b=b0,r=r0,x=0,y=in[p][c],h=1,loops=0;pair<int,int> ans={-1,-1};
    for(;;){
     demand(++loops<=nodes[1-p][r0].rank+2,"nondecreasing internal calls");
     column(H,b,x,y,h);
     if(y<0||y>=H)break;
     int o=find(out[p].begin(),out[p].end(),y)-out[p].begin();demand(o<(int)out[p].size(),"output parity");
     if(x<0){ans={o,product[p][b][r]};demand(nodes[p][ans.second].rank<parent.rank,"parent residual rank");break;}
     auto v=nodes[1-p][r].reply[o];if(v.first<0)break;
     demand(nodes[1-p][v.second].rank<nodes[1-p][r].rank,"child rank decrease");
     r=v.second;y=out[1-p][v.first];h=3;
    }
    demand(ans==parent.reply[c],"declared response differs from literal product");equations++;
   }
  }
 }
 demand(bool(f),"truncated catalog certificate");
 cout<<"{\"catalog_equations\":"<<equations<<",\"catalog_nodes\":"<<trees<<"}"<<endl;
}
void run(long long l,long long r){
 demand(l>=0&&r>=0&&l<=2000&&r<=2000,"literal query exceeds explicit test range");
 vector<int> left={5,6,10,12,17},right={6,10,12,17};
 for(int i=0;i<l;i++){left.push_back(18);left.push_back(29);}
 for(int i=0;i<r;i++){right.push_back(18);right.push_back(29);}
 int seam=left.size();vector<int> colors;
 for(auto it=left.rbegin();it!=left.rend();it++)colors.push_back(31^*it);
 colors.insert(colors.end(),right.begin(),right.end());
 int x=seam,y=3,h=1;long long time=0,cross=0;uint64_t hash=1469598103934665603ULL;
 while(x>=0&&x<(int)colors.size()&&y>=0&&y<5){
  demand(time<100000000,"INCONCLUSIVE literal limit");
  int old=x,b=(colors[x]>>y)&1;colors[x]^=1<<y;
  hash^=(b?'L':'R');hash*=1099511628211ULL;
  h=turn[b][h];x+=dx[h];y+=dy[h];time++;
  if((old<seam)!=(x<seam))cross++;
 }
 ostringstream hs;hs<<hex<<setw(16)<<setfill('0')<<hash;
 cout<<"{\"l\":"<<l<<",\"r\":"<<r<<",\"steps\":"<<time<<",\"pose\":["<<x<<','<<y<<','<<h
     <<"],\"crossings\":"<<cross<<",\"turn_hash\":\""<<hs.str()<<"\",\"columns\":[";
 for(int i=0;i<(int)colors.size();i++){if(i)cout<<',';cout<<colors[i];}cout<<"]}"<<endl;
}
int main(int argc,char**argv){
 try{
  demand(argc==3,"usage: independent catalogs.txt cases.txt");check_catalogs(argv[1]);
  ifstream f(argv[2]);demand(bool(f),"cases unreadable");long long l,r;
  while(f>>l>>r)run(l,r);
 }catch(const exception& e){cerr<<e.what()<<endl;return 1;}
}
