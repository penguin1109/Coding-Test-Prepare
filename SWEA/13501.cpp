#include <iostream>
#include <list>

using namespace std;

int T;
int test_case;
int N, M, L;

int temp;
char c;
int x, y;

int main() {
	cin >> T;
	for (test_case = 1; test_case <= T; ++test_case) {
		cin >> N >> M >> L;
		list<int> arr;
		for (int i = 0; i < N; i++) {
			cin >> temp;
			arr.push_back(temp);
		}
		for (int i = 0; i < M; i++) {
			cin >> c;
			if (c == 'I') {
				cin >> x >> y;
				list<int> temp;
				auto cursor = arr.begin();
				for (int i = 0; i < x - 1; i++) {
					cursor++;
				}
				temp.push_back(y);
				arr.splice(cursor, temp);
			}
			else if (c == 'D') {
				cin >> x;
				auto cursor = arr.begin();
				for (int i = 0; i < x; i++) {
					cursor++;
				}
				arr.erase(cursor);
			}
			else if (c == 'C') {
				cin >> x >> y;
				list<int> temp;
				auto cursor = arr.begin();
				for (int i = 0; i < x; i++) {
					cursor++;
				}
				temp.push_back(y);
				cursor = arr.erase(cursor);

				arr.splice(cursor, temp);
			}
		}

		if (arr.size() < L) {
			cout << "#" << test_case << " " << -1 << endl;
		}
		else {
			for (int i = 0; i < L; i++) {
				arr.pop_front();
			}
			cout << "#" << test_case << " " << arr.front() << endl;

		}
	}
	return 0;
}