#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <stdio.h>
#include <memory.h>

using namespace std;

int N, M, K, x, y, z = 0;

struct _land {
	int tree[11][11]; // �����ϴ� ������ �����ϴ� �迭
	int nutri[11][11] = { 5 }; // �����ϴ� ����� ������ �����ϴ� �迭

	void spring() {

	}
};
int main(int argc, char** argv) {
	cin >> N >> M >> K;
	_land board;
	int n = 0;
	for (int i = 0; i < N; i++) {
		for (j = 0j < N; j++) {
			scanf("%d", &n);
			board.nutri[i] + j += n;
		}
	}
	for (int i = 0; i < M; i++) {
		scanf("%d %d %d", &x, &y, &z); // ������ (x,y) ��ǥ�� ����
		board.tree[x][y] = z;
	}
}