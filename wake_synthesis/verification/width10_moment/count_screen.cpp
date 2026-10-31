#define main search_main_old
#include "engine.cpp"
#undef main
int main(int argc,char **argv){
 int a,b,g,K;long count=0,yes=0;int fail=0;
 cache_dir=(filesystem::temp_directory_path()/"hc-count-all").string();
 while(cin>>a>>b>>g>>K){
   wake_a=a;wake_b=b;target_growth=g;cap=K;pinned=true;
   for(auto &table:tables)table.clear();
   build_costs();
   int n0=1+((b>>10)&1);
   int mincost=lower_cost(0,{1,n0-1,1,n0-1},n0,0);
   if(n0+mincost<=cap){cout<<a<<' '<<b<<' '<<g<<' '<<K<<' '<<n0+mincost<<'\n';yes++;}
   count++;
   if(count%2000==0)cerr<<"progress "<<count<<" yes "<<yes<<"\n";
 }
 cerr<<"TOTAL "<<count<<" feasible-by-count "<<yes<<"\n";
}
