// Separate literal verifier. No Python, project simulator, or search engine.
// Full ordered black sets, signed-vector turns, direct ten-window lookup.
#include <algorithm>
#include <array>
#include <cstdlib>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>
using P = std::pair<long long,long long>;
using Field = std::set<P>;
static void demand(bool v, const std::string& s) { if(!v) throw std::runtime_error(s); }
static P plus(P a,P b){return {a.first+b.first,a.second+b.second};}
static P times(long long n,P a){return {n*a.first,n*a.second};}
static const std::array<P,4> directions={P{0,1},P{1,0},P{0,-1},P{-1,0}};
static int heading(P v){for(int h=0;h<4;++h)if(directions[h]==v)return h;throw std::runtime_error("bad velocity");}
struct Ant {
    Field black; P p={0,0},v={0,1};
    char update(){
        auto it=black.find(p); bool b=(it!=black.end());
        if(b){black.erase(it);v={-v.second,v.first};}
        else {black.insert(p);v={v.second,-v.first};}
        p=plus(p,v); return b?'L':'R';
    }
};
static bool multiple(P x,P d,long long& k){
    int axis=d.first?0:1;long long n=axis?x.second:x.first,z=axis?d.second:d.first;
    if(!z || n%z)return false;k=n/z;return x==times(k,d);
}
// Independently check permanence by evaluating complete parity on every interval,
// not using the Python event-sweep implementation.
static void permanent(const Ant& src,const std::string& word){
    Ant g; g.p=src.p;g.v=src.v;std::vector<P> q;
    for(char c:word){q.push_back(g.p);g.v=(c=='R'?P{g.v.second,-g.v.first}:P{-g.v.second,g.v.first});g.p=plus(g.p,g.v);}
    P d={g.p.first-src.p.first,g.p.second-src.p.second};
    demand(g.v==src.v && d!=P{0,0},"invalid translating plan");
    for(size_t i=0;i<q.size();++i){
        std::vector<long long> writes,hits;std::set<long long> tests={0};
        for(size_t j=0;j<q.size();++j){long long s;P delta={q[j].first-q[i].first,q[j].second-q[i].second};
            if(multiple(delta,d,s)&&(s>0||(s==0&&j<i))){writes.push_back(s);tests.insert(s);if(s>0)tests.insert(s-1);}}
        for(P x:src.black){long long s;P delta={x.first-q[i].first,x.second-q[i].second};
            if(multiple(delta,d,s)&&s>=0){hits.push_back(s);tests.insert(s);tests.insert(s+1);if(s>0)tests.insert(s-1);}}
        if(!tests.empty())tests.insert(*tests.rbegin()+1);
        for(long long k:tests){bool value=src.black.count(plus(q[i],times(k,d)))!=0;
            for(long long s:writes)if(s<=k)value=!value;
            demand(value==(word[i]=='L'),"permanent tail parity mismatch");}
    }
}

static Field shifted(const Field& a,P v){Field r;for(P q:a)r.insert(plus(q,v));return r;}
static void toggle(Field& a,P q){auto i=a.find(q);if(i==a.end())a.insert(q);else a.erase(i);}
static void xor_into(Field& a,const Field& b){for(P q:b)toggle(a,q);}
static bool hits_ray(P p,P q,P d,long long lo){long long j;return multiple({p.first-q.first,p.second-q.second},d,j)&&j>=lo;}
static long long guard_points(const Field& reads,const Field& starts,P stride,long long lo){
    for(P p:reads)for(P q:starts)demand(!hits_ray(p,q,stride,lo),"native universal point/ray guard");
    return (long long)reads.size()*starts.size();
}
static std::vector<P> execute(Ant& a,const std::string& w){std::vector<P> q;for(char c:w){q.push_back(a.p);demand(a.update()==c,"native basis word");}return q;}
static Field odd(const std::vector<P>& q){Field r;for(P p:q)toggle(r,p);return r;}
static Field pointset(const std::vector<P>& q){return Field(q.begin(),q.end());}
static void universal_basis(const std::string& W,const std::string& U,const std::string& V,
                            const std::string& Z,const std::string& O){
    const P d={2,-2};
    const Field P0={{0,-2},{0,-1},{0,0},{1,-1},{2,-1},{2,1},{3,-2},{3,1},{4,-2},{4,0},{5,-1},{5,0},{6,0}};
    const Field D={{0,-3},{0,0},{1,-4},{1,-3},{1,-2},{2,-1},{2,0},{3,0},{6,-1},{7,-1},{7,0},{8,-1}};
    const Field M={{-2,-8},{1,-8},{1,-5},{1,-2},{6,-1},{7,-3}};
    Ant blank;std::vector<P> cr;for(int i=0;i<9977;++i){cr.push_back(blank.p);blank.update();}
    Field E;for(P q:blank.black){q={q.first-blank.p.first,q.second-blank.p.second};E.insert({-q.second,q.first});}xor_into(E,P0);
    demand(E.size()==702,"native blank debris");
    Ant core;core.black=P0;core.v={0,-1};auto wr=execute(core,W);
    Field target=shifted(P0,d);xor_into(target,D);demand(core.black==target,"native full period identity");
    guard_points(E,pointset(wr),d,0);
    Field source_rays;for(P q:M)source_rays.insert(plus(blank.p,{q.second,-q.first}));
    long long pre=guard_points(pointset(cr),source_rays,{-2,-2},32);
    pre+=guard_points(pointset(wr),M,d,1);
    // True inverse reads of the empty state, independently from vector inversion.
    Ant inv;Field ir;
    for(int z=0;z<9;++z){inv.p=plus(inv.p,times(-1,inv.v));ir.insert(inv.p);bool postblack=inv.black.count(inv.p);
        toggle(inv.black,inv.p);inv.v=postblack?P{-inv.v.second,inv.v.first}:P{inv.v.second,-inv.v.first};}
    pre+=guard_points(ir,source_rays,{-2,-2},32);
    Ant begin;begin.v={0,-1};begin.black=P0;xor_into(begin.black,M);
    for(int j=1;j<=32;++j)xor_into(begin.black,shifted(D,times(-j,d)));
    xor_into(begin.black,shifted(E,times(-32,d)));
    auto ur=execute(begin,U);demand(begin.p==P{-1,-1}&&begin.v==P{0,-1},"native U endpoint");
    Field K=P0;xor_into(K,M);xor_into(K,odd(ur));
    Ant ret=begin;auto vr=execute(ret,V);Field R=odd(vr);
    demand(ret.p==plus(begin.p,times(-1,d)) && ret.v==begin.v,"native return displacement");
    Field Q=K;xor_into(Q,shifted(K,d));xor_into(Q,D);xor_into(Q,shifted(R,d));
    demand(K.size()==127 && R.size()==26 && Q.size()==140,"native archive cardinalities");
    Field uv=pointset(ur);auto vs=pointset(vr);uv.insert(vs.begin(),vs.end());
    long long incoming=guard_points(uv,D,times(-1,d),33)+guard_points(uv,E,times(-1,d),32);
    Ant recovery=begin;auto zr=execute(recovery,Z);permanent(recovery,O);
    long long outgoing=guard_points(vs,Q,d,0)+guard_points(pointset(zr),Q,d,0);
    Ant out=recovery;auto oq=execute(out,O);demand(out.p==plus(recovery.p,{-2,-2}),"native outgoing displacement");
    // Cross-sum coordinates solve the two nonparallel diagonal-ray equations.
    for(P v:oq)for(P q:Q){long long jnum=v.first+v.second-q.first-q.second;
        long long rnum=v.first-v.second-q.first+q.second;
        demand(jnum%4 || rnum%4 || jnum<0 || rnum<0,"native infinite archive/suffix collision");}
    std::cout<<"GUARDS "<<pre<<' '<<incoming<<' '<<outgoing<<' '<<(oq.size()*Q.size())<<' '<<Q.size()<<'\n';
}

int main(){try{
    std::string W,U,V,Z,O;std::cin>>W>>U>>V>>Z>>O;
    demand(W.size()==104 && U.size()==1210 && V.size()==116 && Z.size()==4406 && O.size()==104,"bad word sizes");
    std::set<std::string> legal;std::string doubled=W+W;
    for(int i=0;i<104;++i)legal.insert(doubled.substr(i,10));
    demand(legal.size()==84,"standard language mismatch");
    Ant blank;std::string C;for(int i=0;i<9977;++i)C+=blank.update();
    demand(blank.p==P{-15,10} && heading(blank.v)==3 && blank.black.size()==715,"blank reference mismatch");
    permanent(blank,W);
    universal_basis(W,U,V,Z,O);
    int cases;std::cin>>cases;demand(cases>=0 && cases<=10000,"case count");
    const std::array<P,6> seed={P{-87,-55},P{-87,-52},P{-84,-55},P{-82,-61},P{-81,-55},P{-80,-60}};
    for(int c=0;c<cases;++c){
        long long k;std::cin>>k;demand(k>=0 && k<=100000,"finite control range");
        Ant a;Field unread;
        for(P q:seed){q=plus(q,{-2*k,-2*k});a.black.insert(q);unread.insert(q);}
        const long long T=18921+220*k,first_wave=9977+104*(32+k)+1210;
        std::string expected=C;for(long long j=0;j<32+k;++j)expected+=W;expected+=U;
        for(long long j=0;j<k;++j)expected+=V;expected+=Z;
        demand((long long)expected.size()==T,"prefix length");
        std::string history;long long defects=0,motifs=0;
        for(long long t=0;t<T;++t){
            auto it=unread.find(a.p);if(it!=unread.end()){
                demand(a.black.count(a.p)==1 && t<first_wave,"original lifetime was not consumed before wave");unread.erase(it);}
            char letter=a.update();demand(letter==expected[t],"literal word mismatch at k="+std::to_string(k)+" t="+std::to_string(t));
            history+=letter;if(history.size()>10)history.erase(history.begin());
            if(history.size()==10 && !legal.count(history))++defects;
            if(history.size()>=5 && history.compare(history.size()-5,5,"RLRLR")==0)++motifs;
        }
        demand(unread.empty(),"original lifetime not consumed");
        demand(motifs==259+k,"five-factor total");
        demand(a.p==P{-19,30} && heading(a.v)==3,"common endpoint");
        demand(defects==6702+47*k && a.black.size()==(size_t)(1645+24*k),"count or endpoint mass");
        permanent(a,O);
        std::cout<<"CASE "<<k<<' '<<T<<' '<<defects<<' '<<a.p.first<<' '<<a.p.second<<' '<<heading(a.v)<<' '<<a.black.size()<<'\n';
        for(P q:a.black)std::cout<<q.first<<' '<<q.second<<'\n';
    }
    std::cout<<"PASS independent complete fields, turn words and source lifetimes\n";
    return 0;
}catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}}
