// Consecutive-visit rank pruning. Standard-wake coordinates only.
// Node needs fields t,r,k,next,prev,v. The caller has excluded directed cycles.
// The same function is exercised by the independent streaming test harness.
#pragma once
#include <array>
#include <cstdint>
#include <stdexcept>
#include <vector>
inline std::uint64_t rank_checks=0, rank_rejections=0;
template<class Node>
bool consecutive_chain_ranks(const std::vector<Node>& nodes, int cap) {
    if(cap<1 || cap>856 || nodes.size()>static_cast<std::size_t>(cap))
        throw std::runtime_error("rank-check domain");
    static std::array<std::uint64_t,11*(4*856+5)> stamps{};
    static std::array<int,11*(4*856+5)> ranks{};
    static std::uint64_t epoch=0;
    ++rank_checks;
    for(int s=0;s<static_cast<int>(nodes.size());++s) if(nodes[s].prev<0) {
        if(++epoch==0) { stamps.fill(0); epoch=1; }
        int i=s,level=0,visited=0;
        while(i>=0) {
            if(i>=static_cast<int>(nodes.size()) || ++visited>cap)
                throw std::runtime_error("non-path rank-check input");
            const auto& nd=nodes[i];
            const int x=nd.r+2*level;
            if(nd.t < -10 || nd.t>0 || nd.r<0 || nd.r>1 ||
               nd.k<0 || x < -2*cap || x>2*cap+1)
                throw std::runtime_error("rank-check coordinate");
            const int cell=(nd.t+10)*(4*cap+5)+x+2*cap+2;
            if(stamps[cell]==epoch && nd.k!=ranks[cell]+1) {
                ++rank_rejections; return false;
            }
            stamps[cell]=epoch; ranks[cell]=nd.k;
            level+=nd.v; i=nd.next;
        }
    }
    return true;
}
