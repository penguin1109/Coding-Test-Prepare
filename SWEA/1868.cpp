#include <iostream>
#include <queue>
#include <vector>
// 지뢰가 없는 곳을 방문하고 그와 인접한 곳에도 지뢰가 없다면 bfs로 방문 처리를 한다.
// 하지만 클릭해야 하는 최소 갯수를 구하는건데 말이지...
using namespace std;
int T, test_case, N;
char c;
#define MAXN 301
#define MAXCLICK 999999
char map[MAXN][MAXN];
int visited[MAXN][MAXN] = { 0 };

int dx[8] = {-1, -1, -1, 1, 1, 1, 0, 0};
int dy[8] = { -1, 1, 0, -1, 1, 0, -1, 1 };


bool check(int x, int y) {
	for (int dir = 0; dir < 8; dir++) {
		int nx = x + dx[dir];
		int ny = y + dy[dir];
		if (0 <= nx && 0 <= ny && N > nx && N > ny) {
			if (map[nx][ny] == '*') {
				return false;
			}
		}
	}
	return true; // 사방이 지뢰가 없음 -> 연속적으로 숫자로 바뀌어야 함
}

int bfs() {
	int cnt = 0;
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			if (map[i][j] == '.' && visited[i][j] == 0 && check(i, j)) {
				queue<pair<int, int>> q;
				q.push(make_pair(i, j));
				cnt++;
				while (!q.empty()) {
					int x = q.front().first;
					int y = q.front().second;
					visited[x][y] = 1;
					q.pop();
					for (int dir = 0; dir < 8; dir++) {
						int nx = x + dx[dir];
						int ny = y + dy[dir];
						if (0 <= nx && 0 <= ny && N > nx && N > ny) {
							if (map[nx][ny] == '.' && visited[nx][ny] == 0) {
								visited[nx][ny] = 1;
								if (check(nx, ny)) {
									q.push(make_pair(nx, ny));
								}
							}
						}
					}
				}
			}
		}
	}
	return cnt;
}

void init(){
    for (int i = 0 ;i < MAXN;i++){
        for (int j = 0;j<MAXN;j++){
            visited[i][j] = 0;
        }
    }
}
int main() {
	cin >> T;
	for (test_case = 0; test_case < T; test_case++) {
        init();
		cin >> N; // 지뢰찾기를 하는 표의 크기
		for (int i = 0; i < N; i++) {
			for (int j = 0; j < N; j++) {
				cin >> c; // *인 경우만 지뢰가 있음
				map[i][j] = c;
			}
		}
		int answer = bfs();
        for (int i = 0;i<N;i++){
            for (int j = 0;j<N;j++){
                if (map[i][j] == '.' && visited[i][j] == 0){
                    answer += 1;
                }
            }
        }
		cout << "#" << test_case + 1 << " " << answer << endl;

	}
	return 0;
}
