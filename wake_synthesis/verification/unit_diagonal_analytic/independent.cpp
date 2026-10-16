// Independent complete-row audit of the three-layer obstruction.
// Generates all I-element subsets at every analytically allowed length,
// computes ports by actual quarter-turns, and checks all stable-ranked pairs within each fixed path.
// No search period, strip width, timeout or work limit is an input.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <functional>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>
using namespace std;
using Rows=vector<vector<int>>;
const array<pair<int,int>,4> step={{{0,1},{1,0},{0,-1},{-1,0}}};
struct Event {int depth,rank,arrival,heading,outheading;};
struct Graph {vector<Event> e; vector<int> next,previous,delta;};
int heading(int depth,int arrival) {
    return depth%2 ? (arrival?2:0) : (arrival?3:1);
}
int output(int h,int rank) {return (h+(rank%2?3:1))%4;}
int upper_departure(int depth,int rank,int arrival) {
    auto [x,y]=step[output(heading(depth,arrival),rank)];
    return x+y==1;
}
Graph geometry(const Rows& rows) {
    Graph g; map<pair<int,int>,vector<int>> outgoing,incoming;
    for(int d=0;d<(int)rows.size();d++) for(int k=0;k<(int)rows[d].size();k++) {
        int a=rows[d][k],h=heading(d,a),out=output(h,k),i=g.e.size();
        g.e.push_back({d,k,a,h,out});
        auto [ix,iy]=step[h];auto [ox,oy]=step[out];
        outgoing[{d,d-ox-oy}].push_back(i);
        incoming[{d+ix+iy,d}].push_back(i);
    }
    int n=g.e.size();g.next.assign(n,-1);g.previous.assign(n,-1);g.delta.assign(n,0);
    for(auto [edge,src]:outgoing) {
        if(edge.second<0 || edge.second>=(int)rows.size()) continue;
        const auto& dst=incoming[edge];
        if(src.size()!=dst.size()) throw runtime_error("port imbalance");
        for(size_t k=0;k<src.size();k++) {
            int u=src[k],v=dst[k];
            if(g.next[u]!=-1||g.previous[v]!=-1) throw runtime_error("port reused");
            g.next[u]=v;g.previous[v]=u;g.delta[u]=step[g.e[u].outheading].first;
        }
    }
    return g;
}
// Returns 0 for no obstruction, 1 for a closed component, 2 for rank gap,
// and 3 for a stable-ranked pair with impossible time order.
int obstruction(const Rows& rows) {
    auto g=geometry(rows);int n=g.e.size();vector<int> color(n,0);
    for(int s=0;s<n;s++) if(!color[s]) {
        int i=s;while(i>=0&&!color[i]) {color[i]=s+1;i=g.next[i];}
        if(i>=0&&color[i]==s+1) return 1;
        i=s;while(i>=0&&color[i]==s+1) {color[i]=-1;i=g.next[i];}
    }
    vector<vector<int>> paths;vector<int> component(n,-1),xat(n);
    for(int s=0;s<n;s++) if(g.previous[s]<0) {
        int c=paths.size(),x=0,y=-g.e[s].depth;vector<int> path;map<pair<int,int>,int> last;
        for(int i=s;i>=0;i=g.next[i]) {
            if(x+y!=-g.e[i].depth) throw runtime_error("geometric mismatch");
            component[i]=c;xat[i]=x;path.push_back(i);
            pair<int,int> cell={x,y};auto it=last.find(cell);
            if(it!=last.end()&&g.e[i].rank!=it->second+1) return 2;
            last[cell]=g.e[i].rank;
            auto [dx,dy]=step[g.e[i].outheading];x+=dx;y+=dy;
        }
        paths.push_back(path);
    }
    for(const auto& path:paths) {
        // Direct pairwise inequality, not Python's grouped/sorted key test.
        for(int p=0;p<(int)path.size();p++) for(int q=0;q<(int)path.size();q++) {
            int u=path[p],v=path[q];
            if(g.e[u].depth!=g.e[v].depth||g.e[u].rank>=g.e[v].rank) continue;
            int delta=xat[v]-xat[u];
            if(delta>0 || (delta==0 && q<=p)) return 3;
        }
    }
    return 0;
}
int main() {
    vector<Rows> survivors={Rows{vector<int>{0}}};
    cout<<"{\"status\":\"complete\",\"implementation\":\"independent-vector-geometry\",\"rows\":[";
    for(int depth=1;depth<=3;depth++) {
        array<uint64_t,4> counts{};uint64_t generated_subsets=0;int maximum=0;
        vector<Rows> next;
        for(const auto& rows:survivors) {
            int I=0,J=count(rows.back().begin(),rows.back().end(),0);
            for(int k=0;k<(int)rows.back().size();k++) I+=!upper_departure(depth-1,k,rows.back()[k]);
            if(I!=J) throw runtime_error("unbalanced frontier");
            // From n=4(I-ae)+o (even) or n=4ae-o (odd), 0<=ae<=I.
            const int bound=4*I+(depth%2?0:1);
            for(int length=I+1;length<=bound;length++) {
                vector<int> row(length,0);
                function<void(int,int)> subsets=[&](int start,int left) {
                    if(!left) {
                        ++generated_subsets;int up=0;
                        for(int k=0;k<length;k++) up+=upper_departure(depth,k,row[k]);
                        if(up!=J)return;
                        Rows extended=rows;extended.push_back(row);
                        int kind=obstruction(extended);counts[kind]++;
                        int events=0;for(auto &r:extended)events+=r.size();maximum=max(maximum,events);
                        if(!kind) next.push_back(extended);
                        return;
                    }
                    for(int k=start;k<=length-left;k++) {row[k]=1;subsets(k+1,left-1);row[k]=0;}
                };subsets(0,I);
            }
        }
        sort(next.begin(),next.end());
        if(depth>1)cout<<",";
        cout<<"{\"depth\":"<<depth<<",\"tested_subsets\":"<<generated_subsets
            <<",\"candidates\":"<<(counts[0]+counts[1]+counts[2]+counts[3])
            <<",\"survives\":"<<counts[0]<<",\"closed_component\":"<<counts[1]
            <<",\"rank_gap\":"<<counts[2]<<",\"stable_order_reversal\":"<<counts[3]
            <<",\"max_events\":"<<maximum<<",\"survivor_words\":[";
        for(size_t j=0;j<next.size();j++) {
            if(j) cout<<",";
            cout<<"[";
            for(size_t r=0;r<next[j].size();r++) {if(r)cout<<",";cout<<"\"";for(int b:next[j][r])cout<<b;cout<<"\"";}
            cout<<"]";
        }
        cout<<"]}";survivors=move(next);
    }
    cout<<"]}\n";
    if(!survivors.empty()) return 1;
}
