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
* N하의 양의 정수이면서 x와 y로 이루어진 숫자여야 한다.
* 선물할 수 없는 경우에는 -1을 출력한다.
* Q: 근데 그렇다면 x와 y를 모두 한번씩 사용해야 하는 것은 맞을까? -> 해본 결과 그건 상관이 없었다.
* 그런데 문제는 N이 C++의 unsigned long long 자료형도 넘어가게 생겼다는 것이다.
* 그렇다면 백트래킹으로 모든 방법을 할 수는 없는 것인데, N의 범위를 보니 이건 절대 숫자로 입려을 받을 수 없는 상황인 것 같았다.
* 배열이나 string으로 입력을 받아야 하지 않을까??
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
		cin >> N >> x >> y; // N, x, y입력 받아서 (조건에 의하면 무조건 x는 y보다 작은 정수이다.)
		int Nlen = N.size(); // 문자열로 입력 받은 숫자 N의 길이
		int idx = 0;
		if (Nlen == 1 and N[0] < x) { // (예외1) x와 y가 모두 N보다 큰 경우 -> -1
			cout << "#" << test_case << " " << "-1" << endl;
			continue;
		}
		if ((N[0] < y and x == '0') or (N[0] < x)) { // (예외2) answer의 첫번째의 x와 y 모두 지정 될 수 없는 경우
			for (int i = 0; i < Nlen - 1; i++) {
				answer += y;
			}
			if (answer.size() == 0 or answer[0] == '0') { // 그럼에도 불구하고 불가능한 상황이라면, 예를 들면 
				// N이 1자리수인 경우
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
			if (char(N[idx]) < x) {// 이 경우에 불가능하다면 다시 반복한다.
				if (small_idx == -1) { // 최선의 선택을 하다가 되돌아갈 선택 사항이 없는 경우
					answer = "";
					for (int i = 0; i < Nlen - 1; i++) {
						answer += y;
					}
					break;
				}
				idx = small_idx;
				// cout << small_idx;
				answer = answer.substr(0, idx); // idx번째까지의 문자열 사용
				answer += x; // 작은 수로 교체
				smaller = true;
			}
			else if (char(N[idx]) > y) {
				for (int i = idx; i < Nlen; i++) {
					answer += y;
				} // y의 반복으로 구성해도 N보다 작을 수 밖에 없다.
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
			else if (char(N[idx]) == y) { // 더 큰수와 같은 경우에는 꼭 크게 한다고 좋은 것은 아님
				answer += y;// 우선은 큰수를 사용하여본다.
				small_idx = idx;
			}
			idx += 1;

		}
		if (answer.size() == 0 or answer[0] == '0') { // 양의 정수이기도 해야 한다
			cout << "#" << test_case << " " << "-1" << endl;
		}

		else {
			cout << "#" << test_case << " " << answer << endl; // 정답 출력
		}
	}
	return 0;
}