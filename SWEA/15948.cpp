#include <iostream>
#include <queue>
#include <cstring>
#include <cstdio>
using namespace std;

char board[100 + 2][20 + 2];
int row, col;
int visit[100 + 2][20 + 2]; // 방문했으면 1로 표시
int bought[26 + 2]; // 해당 알파벳의 물건을 구매했다면 1로 표시
int T; // text case개수 저장을 위해서
int answer = 0; // 제일 많이 살 수 있는 개수 저장

typedef struct
{
	int x, y;
	int cnt; // 제일 많이 모은 개수
}_checker;
queue<_checker> Q;

void input() {
	memset(board, 'A', sizeof(board));
	memset(visit, 0, sizeof(visit));
	memset(bought, 0, sizeof(bought));
	answer = 0;

	Q = {};

	scanf("%d %d", &row, &col);
	for (int r = 1; r <= row; r++) {
		scanf("%s", &board[r][1]);
	}
	Q.push({ 1,1, 1 });
	visit[1][1] = 1;
	bought[board[1][1] - 65] = 1;
}

void debug() {
	for (int r = 1; r <= row; r++) {
		for (int c = 1; c <= col; c++) {
			printf("%c ", board[r][c]);
		}
		printf("\n");
	}
}
void dfs(_checker data)
{
	int dir_x[4] = { -1, 1, 0, 0 };
	int dir_y[4] = { 0,0,-1,1 };


	for (int d = 0; d < 4; d++) {
		int nx = data.x + dir_x[d];
		int ny = data.y + dir_y[d];
		if (nx > row or nx < 1) {
			if (answer < data.cnt) { answer = data.cnt; };
			continue;
		}
		if (ny > col or ny < 1) {
			if (answer < data.cnt) { answer = data.cnt; };
			continue;
		}

		char ntype = board[nx][ny];
		if (bought[ntype - 65] == 0 and visit[nx][ny] == 0) {
			bought[ntype - 65] = 1;
			visit[nx][ny] = 1;
			_checker ndata = { nx, ny, data.cnt + 1 };
			dfs(ndata);
			// 다시 방문 여부를 기록한 값들을 원상 복귀 시켜 준다.
			bought[ntype - 65] = 0;
			visit[nx][ny] = 0;
		}
		else {
			if (answer < data.cnt) {
				answer = data.cnt;
			}
		}
	}
}
int main(int argc, char** argv) {
	int test_case;
	int T;
	freopen("input.txt", "r", stdin); // input.txt 파일에서 테스트 케이스를 받아온다.
	setbuf(stdout, NULL);
	scanf("%d", &T); // testcase의 개수를 입력으로 받기

	int dx[4] = { -1,1,0,0 }; int dy[4] = { 0,0,1,-1 }; // 호설이가 이동을 할 수 있는 4개의 방향을 지정해 준다.
	for (test_case = 1; test_case <= T; ++test_case)
	{
		input();
		//debug();
		_checker init = { 1,1,1 };
		dfs(init);
		printf("%c%d %d\n", '#', test_case, answer);
	}
	return 0;
}

