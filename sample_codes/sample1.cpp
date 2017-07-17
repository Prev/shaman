#include <math.h>
#include <iostream>
#include <algorithm>
#include <vector>
#include <queue>
#include <unordered_map>

#define INF 1987654321
#define SOURCE_VAL 1001
#define SINK_VAL 1002


using namespace std;


typedef int node_value;


bool is_prime(int n) {
	if (n == 1) return false;
	
	for (int i=2; i<=sqrt(n); i++)
		if (n % i == 0) return false;
	
	return true;
}
bool used[1005] = {false, };


struct Node;
struct Edge;

struct Edge {
	Node* target;
	Edge* reverse;
	int capacity, flow;
	
	Edge() {
		this->flow = 0;
	}
	
	Edge(Node* target, int capacity) {
		this->target = target;
		this->capacity = capacity;
		this->flow = 0;
	}
	
	int getRestCapacity() {
		return capacity - flow;
	}
	void push(int amt){
		flow += amt;
		this->reverse->flow -= amt;
	}
};

struct Node {
	vector<Edge*> edges;
	node_value value;
	
	void connectTo(Node* target, int capacity) {
		Edge *e = new Edge(target, capacity);
		Edge *e_rev = new Edge(this, 0);
		
		e->reverse = e_rev;
		e_rev->reverse = e;
		
		this->edges.push_back( e );
		target->edges.push_back( e_rev );
	}
};

int networkFlow(Node* source, Node* sink) {
	int totalAmount = 0;
	
	while (true) {
		queue< Node* > que;
		unordered_map<Node*, Edge*> track;
		
		que.push( source );
		
		// 경로 탐색
		while (!que.empty() && track[sink] == nullptr) {
			Node* here = que.front();
			que.pop();
			
			for (int k=0; k<here->edges.size(); k++) {
				Edge* e = here->edges[k];
				
				if (here != source && here != sink && e->target != source && e->target != sink) {
					if (!is_prime(here->value + e->target->value)) continue;
					if (used[e->target->value]) continue;
					used[here->value] = true;
				}
				
				if (e->getRestCapacity() > 0 && track[e->target] == nullptr) {
					que.push( e->target );
					track[ e->target ] = e->reverse;
				}
			}
		}
		
		if (track[sink] == nullptr) break;
		
		// 최소 유량 얻음
		int amount = INF;
		for (Node* n = sink; n != source; n = track[n]->target)
			amount = min(amount, track[n]->reverse->getRestCapacity());
		
		// 유량 갱신
		for (Node* n = sink; n != source; n = track[n]->target) {
			printf("%d -> ", n->value);
			track[n]->push( -amount );
		}
		printf("\n");
		
		totalAmount += amount;
	}
	
	return totalAmount;
}



int main() {
	int N;
	scanf("%d", &N);
	
	Node* source = new Node;
	Node* sink = new Node;
	
	vector<Node*> vec1(N);
	vector<Node*> vec2(N);
	
	source->value = SOURCE_VAL;
	sink->value = SINK_VAL;
	
	for (int i=0; i<N; i++) {
		int d; scanf("%d", &d);
		
		vec1[i] = new Node;
		vec1[i]->value = d;
		source->connectTo(vec1[i], N/2);
		
		vec2[i] = new Node;
		vec2[i]->value = d;
		vec2[i]->connectTo(sink, N/2);
	}
	
	for (int i=0; i<N; i++) {
		for (int j=i+1; j<N; j++) {
			vec1[i]->connectTo( vec2[j], 1 );
		}
	}
	
	int ret = networkFlow(source, sink);
	printf("%d", ret);
	
	return 0;
}


