#include <iostream>
#include <vector>
#include <list>

# define MAXN 200

using namespace std;

int test_case;
int N;
int n, l, r;
char c;

struct Node {
	char data;
	int children[2] = { -1 };
};


Node nodes[MAXN];
list<char> formula;
int formCnt;
int valid = 1;

void post_order(int idx) {
	if (nodes[idx].children[0] != -1) {
		post_order(nodes[idx].children[0]);
	}
	if (nodes[idx].children[1] != -1) {
		post_order(nodes[idx].children[1]);
	}
	formCnt++;
	formula.push_back(nodes[idx].data);
}

int main() {
	for (test_case = 1; test_case <= 10; ++test_case) {
		cin >> N;
		valid = 1;
		for (int i = 1; i <= N; ++i) {
			cin >> n >> c;
			if (i <= N / 2) { // 사칙연산 기호여야 함
				int left, right;
				if (i == N / 2 && N % 2 == 0) {
					cin >> left;
					valid = 0; // 이부분은 그냥 valid = 0으로 먼저 둬도 상관이 없다.왜냐면 연산이 유효하려면 트리는 무조건 완전 이진 트리여야 하기 때문이다.
				}
				else {
					cin >> left >> right;
				}
				if (c >= '0' && c <= '9') {
					valid = 0;
				}
			}
			else { // 남은 N/2개는 무조건 leaf node라서 당연히 자식 노드가 없다.
				if (!(c >= '0' && c <= '9')) {
					valid = 0;
				}
			}
		}
		// 무조건 트리는 완전 binary tree이고 따라서 정점의 개수가 N이면 N/2번째 정점까지는 자식 노드를 갖는다.

		cout << "#" << test_case << " " << valid << endl;
	}

	return 0;
}