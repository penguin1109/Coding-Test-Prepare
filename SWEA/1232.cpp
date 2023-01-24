#include <iostream>
#include <string>
#define MAXN 1000
using namespace std;
int test_case;
int N;

int n;
string c;

struct Node {
	int parent = -1;
	double number = 0;
	string calc;
	int children[2] = { 0 };
};

Node formula[MAXN];

void calculate(int idx) {
	Node current = formula[idx];
	Node left = formula[current.children[0]];
	Node right = formula[current.children[1]];

	if (current.calc == "+")formula[idx].number = (left.number) + (right.number);
	else if (current.calc == "*")formula[idx].number = (left.number) * (right.number);
	else if (current.calc == "/")formula[idx].number = (left.number) / (right.number);
	else if (current.calc == "-") formula[idx].number = (left.number) - (right.number);

	if (current.parent == -1) {
		//cout << idx << " " << current.calc << endl;
		return;
	}
	calculate(current.parent);
	if (idx - 1 > N / 2) {
		calculate(idx - 2);
	}
	// calculate(idx - 2);
}

int main() {
	for (test_case = 1; test_case <= 10; ++test_case) {
		cin >> N; // 정점의 개수

		for (int i = 1; i <= N; i++) {
			cin >> n >> c;
			int children[2] = { 0 };
			if (cin.get() != '\n') {
				cin >> children[0];
				if (cin.get() != '\n') {
					cin >> children[1];
				}
			}
			if (children[0] == 0) {
				formula[i - 1].number = stof(c);
			}
			formula[i - 1].calc = c;
			formula[i - 1].children[0] = children[0] - 1;
			formula[i - 1].children[1] = children[1] - 1;
			if (children[0] != 0) {
				formula[children[0] - 1].parent = i - 1;
				formula[children[1] - 1].parent = i - 1;
			}


		}
		calculate(N - 1);
		//for (int i = 0; i < N; i++) {
			//cout << formula[i].number << " ";
		//}
		cout << "#" << test_case << " " << formula[0].number << endl;
	}
	return 0;
}