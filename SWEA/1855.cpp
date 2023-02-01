using namespace std;

#include <iostream>
#include <algorithm>
#include <queue>
#include <vector>
#include <cstring>

long long answer; // 정답 최소 횟수 (int형으로 저장하면 stack overflow가 발생함)
int T, test_case, N, n;

#define MAXN 100005
int depth[MAXN];
int ancestor[MAXN][23]; // 2 ^ 23 >= 10 ^ 5이기 때문에 최대 ancestor의 탐색 깊이는 넉넉 잡아서 23이 될 수 있는 것이다.
bool check[MAXN];
vector<vector<int>> Graph;

void save_ancestor() { // 각각의 노드의 루트 노드까지의 조상을 가까이 있는 순으로 저장한다.
	for (int i = 1; i <= 20; i++) {
		for (int j = 0; j < N;  j++) {
			// j의 2^(i-1) 번째 조상의 2^(i-1)번째 조상이 j의 2^i번째 조상과 똑같다는 뜻이다.
			ancestor[j][i] = ancestor[ancestor[j][i - 1]][i - 1]; // 부모의 부모 정보를 저장함
			//cout << ancestor[j][i] << " ";
		}
		//cout << endl;
	}
}

int lca(int a, int b) {
	if (depth[b] > depth[a]) swap(a, b); // a의 깊이가 더 깊도록 swap
	for (int i = 19; i >= 0; i--) { // 이제 a를 올려서 a와 b 노드의 깊이를 맞춰준다,
		if ((depth[a] - depth[b]) >= (1 << i)) a = ancestor[a][i];
	} // 높이를 동일하게 만들어 줄 때 까지 기다린다.
	if (a == b) return a;
	// a와 b가 다르다면 현재 깊이가 같으니 깊이를 계속 올려서 서로 다른 노드의 조상이 같아지는 순간까지 반복한다.
	// 즉, 서로 다른 노드 (2,3)의 조상이 1로 같다면 lca = ancestor[2][0]에 의해서 2의 조상이 1임을 알 수 있고,
	// ancestor[3][0]에 의해서 3의 조상이 1임을 알수 있어서 이때 알고리즘이 끝난다.
	for (int i = 19; i >= 0; i--) { // 최대 깊이로부터 시작하기 때문에 모든 노드에 대해서 조사가 가능하다.
		if (ancestor[a][i] != ancestor[b][i]) { // 서로 같은 조상이 나오기 전까지 반복을 하고
			a = ancestor[a][i]; // a의 2^i번째 조상 -> 다르니까 a가 그 조상이 되는 것이다.
			b = ancestor[b][i]; // b의 2^i번째 조상 -> 다르니까 b가 그 조상이 되는 것이다.

		}
	}
	return ancestor[a][0]; // 서브 트리에서 만나지 못해도 결국에는 LCA는 루트 노드가 될 것이다.
}
int LCA(int a, int b) {
	int da = depth[a];
	int db = depth[b];
	//cout << "A B" << a << " " << b << endl;
	if (da != db) {
		// 높이가 같으면 높이를 바꿔줄 필요가 없음
		
		if (da < db) {
			int temp = a;
			a = b;
			b = temp;
			da = depth[a]; db = depth[b];
		}
		int temp = a;
		for (int i = 19; i>=0;i--) {
			if (depth[a] - depth[b] >= (1 << i)) {
				a = ancestor[a][i];
			};
			
		}
	}
	if (a == b) {
		return a;
	}
	// 이제 두 노드의 높이가 동일하니 같이 올라가며 찾아주면 된다.
	for (int i = 19; i >= 0;i--) {
		int pa = ancestor[a][i];
		int pb = ancestor[b][i];
		
		if (pa != pb) {
			a = ancestor[a][i];
			b = ancestor[b][i];
		}
	}
	return ancestor[a][0];
}

void save_info() {
	queue<pair<int, int>> dq;
	dq.push(make_pair(0, 0));
	check[0] = true; // 루트 노드 부터 탐색시작
	while (!dq.empty()) {
		int idx = dq.front().first;
		int order = dq.front().second;
		dq.pop();
		depth[idx] = order;
		for (int i = 0; i < Graph[idx].size(); i++) {
			int child = Graph[idx][i];
			if (check[child] == false) {
				check[child] = true;
				ancestor[child][0] = idx;
				depth[child] = order + 1;
				dq.push(make_pair(child, order + 1));
			}
		}
	}
}

void bfs() {
	memset(check, 0, sizeof(check));
	vector<int> vt;
	queue<int> q;
	q.push(0);
	check[0] = true;
	answer = 0;
	while (!q.empty()) {
		int temp = q.front();
		q.pop();
		vt.push_back(temp);
		for (int i = 0; i < Graph[temp].size(); i++) {
			int child = Graph[temp][i];
			if (check[child] == false) {
				check[child] = true;
				q.push(child);
			}
		}
	}
	for (int i = 0; i < N - 1; i++) {
		int l = LCA(vt[i], vt[i + 1]); // LCA(vt[i], vt[i + 1]);
		long long a = depth[vt[i]] - depth[l];
		long long b = depth[vt[i + 1]] - depth[l];
		//cout << a << b << endl;
		answer += (a + b);
	}

}
int main() {
	cin >> T;
	for (test_case = 0; test_case < T; test_case++) {
		memset(check, 0, sizeof(check));
		memset(depth, 0, sizeof(depth));
		memset(ancestor, 0, sizeof(ancestor));
		Graph.clear();
		cin >> N;
		Graph.resize(N + 3); // 이 부분이 너무나도 중요했었다. Graph는 vector인데 size를 할당을 해 주어야 하기 때문이다.
		for (int i = 1; i < N; i++) {
			cin >> n;
			Graph[n - 1].push_back(i);
		}
		for (int i = 0; i < N; i++) {
			sort(Graph[i].begin(), Graph[i].end()); // 번호가 작은 노드부터 뽑아야 하기 때문에 정렬
		}
		save_info();
		save_ancestor();
		bfs();
		cout << "#" << test_case + 1 << " " << answer << endl;


	
	}
}
