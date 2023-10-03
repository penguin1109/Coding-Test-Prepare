#include <iostream>
#include <vector>

using namespace std;
int test_case;
int V, E, a, b;

#define MAXN 10010

struct Node {
	int key = 0;
	int parent;
	int children[2] = { -1,-1 };
};

int all_parent[MAXN] = { -1 };
int cnt = 0;
void traverse(int idx, Node nodes[]) {
	if (nodes[idx].children[0] != -1) {
		traverse(nodes[idx].children[0], nodes);
	}
	if (nodes[idx].children[1] != -1) {
		traverse(nodes[idx].children[1], nodes);
	}
	cnt++;
	//cout << "traverse" << idx;
}
int main() {
	int T;
	cin >> T;
	for (test_case = 1; test_case <= T; ++test_case) {
		Node nodes[MAXN];
		int tree_size = 0;
		int tree_root = 0;
		cin >> V >> E >> a >> b;
		a -= 1; b -= 1;
		int parent = 0; int child = 0;
		for (int i = 0; i < E; i++) {
			cin >> parent >> child;
			if (nodes[parent - 1].children[0] != -1) {
				nodes[parent - 1].children[1] = child - 1;
			}
			else {
				nodes[parent - 1].children[0] = child - 1;
			}
			nodes[child - 1].parent = parent - 1;
			all_parent[child - 1] = parent - 1;
		}
		vector<int> A;
		vector<int> B;

		int now = a;
		while (now != -1) {
			//cout << now << " ";
			A.push_back(now);
			now = all_parent[now];
		}
		now = b;
		while (now != -1) {
			//cout << now << " ";
			B.push_back(now);
			now = all_parent[now];
		}
		// 제일 가까운 조상 찾기
		bool isFind = false;
		for (int i = 0; i < A.size(); i++) {
			if (isFind) break;
			for (int j = 0; j < B.size(); j++) {
				if (A.at(i) == B.at(j)) {
					tree_root = A.at(i); // 제일 가까운 조상을 tree_root에 저장해둠
					isFind = true;
					break;
				}
			}
		}
		//cout << tree_root;
		cnt = 0;
		traverse(tree_root, nodes);
		cout << "#" << test_case << " " << tree_root + 1 << " " << cnt << endl;

	}
	return 0;
}