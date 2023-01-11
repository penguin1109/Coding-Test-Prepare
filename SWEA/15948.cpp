#include <iostream>
#include <queue>
#include <cstring>
#include <cstdio>
using namespace std;

char board[100 + 2][20 + 2];
int row, col;
int visit[100 + 2][20 + 2]; // �湮������ 1�� ǥ��
int bought[26 + 2]; // �ش� ���ĺ��� ������ �����ߴٸ� 1�� ǥ��
int T; // text case���� ������ ���ؼ�
int answer = 0; // ���� ���� �� �� �ִ� ���� ����

typedef struct
{
	int x, y;
	int cnt; // ���� ���� ���� ����
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
			// �ٽ� �湮 ���θ� ����� ������ ���� ���� ���� �ش�.
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
	freopen("input.txt", "r", stdin); // input.txt ���Ͽ��� �׽�Ʈ ���̽��� �޾ƿ´�.
	setbuf(stdout, NULL);
	scanf("%d", &T); // testcase�� ������ �Է����� �ޱ�

	int dx[4] = { -1,1,0,0 }; int dy[4] = { 0,0,1,-1 }; // ȣ���̰� �̵��� �� �� �ִ� 4���� ������ ������ �ش�.
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

