using namespace std;
#include <algorithm>
#include <iostream>
#include <cstring>
#include <vector>
#define MAXN 1005

int test_case, T, N, x,y;
double E;
int p[MAXN];
bool visit[MAXN][MAXN] = { false };
long long dist[MAXN][MAXN];
vector<pair<pair<long long, long long>, long long>> edges;

struct Tunnel {
	long long x;
	long long y;
	bool used=false;
	Tunnel() {};
	Tunnel(long long x, long long y, bool used) : x(x), y(y), used(used) {};
}tunnels[MAXN];

// 그냥 모든 경우를 다 한다면 당연히 시간초과가 날 수 밖에 없다.
// 정말 다익스트라 알고리즘을 사용해야 하는건가
/* 크루스칼 알고리즘을 사용하는 문제였다.
* 딱 문제 설명을 읽으면 알겠지만 "모든 섬을 연결하는 최단 거리"를 구하는 문제이기 때문에 MST, 즉 최소 신장 트리를 구하는 문제였던 것이다
* 그런데 여기서 이제 만약에 간선의 개수가 적은 편이라면 Prim Algorithm을 사용하는 것도 나쁘지 않다.
* 어쨌든 뭔가 더 오래 걸렸던 이유는 C++의 sorting이나 pair, vector등이 충분히 익숙하지 않았기 때문인 것 같다.
* 예를 들면 sort를 하는 경우 어떤 값을 기준으로 정렬을 하는지 따로 함수로 정의를 해 줄 수 있다.
* 그리고 MST알고리즘의 경우 그리디 기반인데, 결국에는 간선들의 가중치가 작은것 부터 정렬을 하고, 이때 간선을 선택하는 기준은 cycle이 생기는지 아닌지이다.
* cycle이 생기려면 새로 추가하려는 간선의 두 노드들이 이미 연결이 되어 있는, 즉 부모 노드가 같은 것이다. 
* 초기 부모 배열을 자기 자신으로 바꿔놓고, 트리의 개념으로 살펴볼 때 union 함수는 트리를 합치는 것이고, find의 경우에는 서브 트리의 루트를 찾는 것이다.
* 
*/
void cal_dist() {
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			if (i == j) {
				dist[i][j] = 0;
			}
			Tunnel a = tunnels[i];
			Tunnel b = tunnels[j];
			long long dx = (a.x - b.x) * (a.x - b.x);
			long long dy = (a.y - b.y) * (a.y - b.y);
			long long cost = (dx + dy);
			// cout << i << " " << j << " COST: " << cost << endl;
			dist[i][j] = cost;
			dist[j][i] = cost; // 양방향 그래프이기 때문에 두번씩 distance 그래프에 거리 정보를 저장해 준다.
		}
		
	}
	for (int i = 0; i < N; i++) {
		for (int j = i+1; j < N; j++) {
			edges.push_back(make_pair(make_pair(i, j), dist[i][j]));
		}
	}
}

int find_parent(int x) {
	if (p[x] == x) {
		return x;
	}
	return p[x] = find_parent(p[x]);
}

void union_parent(int a, int b) {
	a = find_parent(a);
	b = find_parent(b);
	if (a < b) p[b] = a; // 그냥 임의로 더 작은 수가 부모일것이라고 가정을 해 놓고 번호가 작은 노드를 부모로 설정한다.
	else p[a] = b;
}

bool cmp(pair<pair<int, int>, long long> p1, pair<pair<int, int>, long long> p2) {
	return p1.second < p2.second;
}





int main() {
	cin >> T;
	for (test_case = 0; test_case < T; test_case++) {
		cin >> N; // 섬의 개수
		memset(visit, false, sizeof(visit));
		
		int n;
		for (int i = 0; i < 2; i++) {
			for (int j = 0; j < N; j++) {
				cin >> n;
				if (i == 0) tunnels[j].x = n;
				else tunnels[j].y = n;
			}
		}
		for (int i = 0; i < N; i++) {
			p[i] = i; // 부모 배열 초기화
		}
		cin >> E; // 환경 부담 세율
		cal_dist();
		sort(edges.begin(), edges.end(), cmp); // 거리 기준으로 정렬하도록 한다.

		int edge_cnt = 0;
		double answer = 0;
		for (const auto edge: edges) {
			long long dist = edge.second;
			int i1 = edge.first.first;
			int i2 = edge.first.second;
			if (find_parent(i1) == find_parent(i2)) {
				continue;
			}
			union_parent(i1, i2);
			answer += dist * E;
			edge_cnt += 1;


		}

		long long out = round((answer * 10) / 10);
		cout << "#" << test_case + 1 << " " << out << endl;
	}
}
