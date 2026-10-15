// Exercise the exact predicate compiled into the enumerator, not a copied rule.
#define main enumerator_main
#include "generated.cpp"
#undef main

int main() {
    int n;
    while (std::cin >> n >> cap) {
        ns.clear();
        for (int i=0;i<n;++i) {
            Node node{};
            std::cin >> node.t >> node.r >> node.k >> node.next >> node.prev >> node.v;
            ns.push_back(node);
        }
        std::cout << feasible() << '\n';
    }
}
