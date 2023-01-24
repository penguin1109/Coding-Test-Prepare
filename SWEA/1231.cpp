#include <iostream>
#include <stdio.h>
#include <sstream>
#include <vector>

#define MAXN 100
using namespace std;

int test_case;
int N; // 각 트리가 갖는 정점의 총 개수
int n, l, r;
char c;
string s;





Node nodes[MAXN];

struct Node {
	char data;
	int children[2] = { -1 };
};

char text[MAXN];
int textCnt;

void InOrder(int idx) {
	if (nodes[idx].children[0] != -1) {
		InOrder(nodes[idx].children[0]);
	} // left sub tree 끝까지 탐색
	text[textCnt++] = nodes[idx].data; // 중간에 현재 노드의 값을 저장한다.
	if (nodes[idx].childern[1] != -1) {
		InOrder(nodes[idx].children[1]);
	} // right sub tree 끝까지 탐색
}

int main() {
	for (test_case = 1; test_case <= 10; ++test_case) {
		vector<string> alpha;
		cin >> N;
		for (int i = 0; i < N; i++) {
			cin >> n;
			n--;
			cin >> c;
			int children[2] = { 0, };
			if (cin.get() != '\n') {
				cin >> children[0];
				if (cin.get() != '\n') {
					cin >> children[1];
				}
			}
			children[0] --; children[1]--;
			nodes[n].data = c;
			nodes[n].children[0] = children[0]; // left에 있는 노드의 번호 저장
			nodes[n].children[1] = children[1]; // right에 있는 노드의 번호 저장

		}
		textCnt = 0; // 여기서 int textCnt라고 새롭게 정의를 해 버리면 그냥 
		InOrder(0);
		cout << "#" << test_case << " ";
		for (int i = 0; i < textCnt; i++) {
			cout << text[i];
		}
		cout << endl;

	}
	return 0;
}