#define _CRT_SECURE_NO_WARNINGS
#include <cstdio>
#include <math.h>
#include <iostream>
#include <vector>
#include <queue> 
#include <algorithm> // sort() 알고리즘을 위해서 필요했음
using namespace std;

int test_case;
int T;
int dump;
int answer;
/*
* 매우 간단한 문제였다. (아무래도 문제 해결 기본 문제 1일차니까)
* 어쨌든 python으로만 하다가 오랜만에 C++을 사용하려니 사용법이 익숙하지가 않았다.
* vector, queue, priority_queue, struct등의 라이브러리들에 익숙해지게 공부를 해야 할 것 같다.

*/
int main(int argc, char** argv) {
	cin >> T;
	for (test_case = 1; test_case <= T; test_case++) {
		cin >> dump; // 덤프를 할 수 있는 정해진 횟수
		vector<int> v;
		for (int i = 0; i < 100; i++) {
			int tmp;
			cin >> tmp;
			v.push_back(tmp);
		}

		for (int j = 0; j < dump; j++) {
			sort(v.begin(), v.end());
			if (v.back() - v.front() <= 1) {
				break;
			}
			v[0] ++;
			v[99] --;
		}
		sort(v.begin(), v.end());
		cout << "#" << test_case << " " << v.back() - v.front() << endl;
	}
	return 0;
}