#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <cstdio>
#include <cstring>
#include <algorithm>
#include <string>
#include <math.h>
#include <stdlib.h>
using namespace std;
/*
* N���� ���� �����̸鼭 x�� y�� �̷���� ���ڿ��� �Ѵ�.
* ������ �� ���� ��쿡�� -1�� ����Ѵ�.
* Q: �ٵ� �׷��ٸ� x�� y�� ��� �ѹ��� ����ؾ� �ϴ� ���� ������? -> �غ� ��� �װ� ����� ������.
* �׷��� ������ N�� C++�� unsigned long long �ڷ����� �Ѿ�� ����ٴ� ���̴�.
* �׷��ٸ� ��Ʈ��ŷ���� ��� ����� �� ���� ���� ���ε�, N�� ������ ���� �̰� ���� ���ڷ� �Է��� ���� �� ���� ��Ȳ�� �� ���Ҵ�.
* �迭�̳� string���� �Է��� �޾ƾ� ���� ������??
*/
int test_case;
int T;
int Nlen;

void solution(string curr, int idx, string N, char x, char y) {
	if (Nlen == idx) {

	}
	if (char(N[idx]) < x) {

	}
}

int main(int argc, char** argv) {
	freopen("input.txt", "r", stdin);
	cin >> T;
	for (test_case = 1; test_case <= T; ++test_case) {
		string N, answer = "";
		char x, y;
		bool smaller = false;
		int small_idx = -1;
		cin >> N >> x >> y; // N, x, y�Է� �޾Ƽ� (���ǿ� ���ϸ� ������ x�� y���� ���� �����̴�.)
		int Nlen = N.size(); // ���ڿ��� �Է� ���� ���� N�� ����
		int idx = 0;
		if (Nlen == 1 and N[0] < x) { // (����1) x�� y�� ��� N���� ū ��� -> -1
			cout << "#" << test_case << " " << "-1" << endl;
			continue;
		}
		if ((N[0] < y and x == '0') or (N[0] < x)) { // (����2) answer�� ù��°�� x�� y ��� ���� �� �� ���� ���
			for (int i = 0; i < Nlen - 1; i++) {
				answer += y;
			}
			if (answer.size() == 0 or answer[0] == '0') { // �׷����� �ұ��ϰ� �Ұ����� ��Ȳ�̶��, ���� ��� 
				// N�� 1�ڸ����� ���
				cout << "#" << test_case << " " << "-1" << endl;
			}
			else {
				cout << "#" << test_case << " " << answer << endl;
			}
			continue;
		}

		while (idx < Nlen) {
			if (smaller) {
				for (int i = idx; i < Nlen; i++) {
					answer += y;
				}
				break;
			}
			if (char(N[idx]) < x) {// �� ��쿡 �Ұ����ϴٸ� �ٽ� �ݺ��Ѵ�.
				if (small_idx == -1) { // �ּ��� ������ �ϴٰ� �ǵ��ư� ���� ������ ���� ���
					answer = "";
					for (int i = 0; i < Nlen - 1; i++) {
						answer += y;
					}
					break;
				}
				idx = small_idx;
				// cout << small_idx;
				answer = answer.substr(0, idx); // idx��°������ ���ڿ� ���
				answer += x; // ���� ���� ��ü
				smaller = true;
			}
			else if (char(N[idx]) > y) {
				for (int i = idx; i < Nlen; i++) {
					answer += y;
				} // y�� �ݺ����� �����ص� N���� ���� �� �ۿ� ����.
				idx = Nlen;
				break;
			}
			else if (char(N[idx]) > x and char(N[idx]) < y) {
				answer += x;
				smaller = true;
			}
			else if (char(N[idx]) == x) {
				answer += x;
			}
			else if (char(N[idx]) == y) { // �� ū���� ���� ��쿡�� �� ũ�� �Ѵٰ� ���� ���� �ƴ�
				answer += y;// �켱�� ū���� ����Ͽ�����.
				small_idx = idx;
			}
			idx += 1;

		}
		if (answer.size() == 0 or answer[0] == '0') { // ���� �����̱⵵ �ؾ� �Ѵ�
			cout << "#" << test_case << " " << "-1" << endl;
		}

		else {
			cout << "#" << test_case << " " << answer << endl; // ���� ���
		}
	}
	return 0;
}