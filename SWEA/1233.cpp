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
			if (i <= N / 2) { // ��Ģ���� ��ȣ���� ��
				int left, right;
				if (i == N / 2 && N % 2 == 0) {
					cin >> left;
					valid = 0; // �̺κ��� �׳� valid = 0���� ���� �ֵ� ����� ����.�ֳĸ� ������ ��ȿ�Ϸ��� Ʈ���� ������ ���� ���� Ʈ������ �ϱ� �����̴�.
				}
				else {
					cin >> left >> right;
				}
				if (c >= '0' && c <= '9') {
					valid = 0;
				}
			}
			else { // ���� N/2���� ������ leaf node�� �翬�� �ڽ� ��尡 ����.
				if (!(c >= '0' && c <= '9')) {
					valid = 0;
				}
			}
		}
		// ������ Ʈ���� ���� binary tree�̰� ���� ������ ������ N�̸� N/2��° ���������� �ڽ� ��带 ���´�.

		cout << "#" << test_case << " " << valid << endl;
	}

	return 0;
}