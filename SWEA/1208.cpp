#define _CRT_SECURE_NO_WARNINGS
#include <cstdio>
#include <math.h>
#include <iostream>
#include <vector>
#include <queue> 
#include <algorithm> // sort() �˰����� ���ؼ� �ʿ�����
using namespace std;

int test_case;
int T;
int dump;
int answer;
/*
* �ſ� ������ ��������. (�ƹ����� ���� �ذ� �⺻ ���� 1�����ϱ�)
* ��·�� python���θ� �ϴٰ� �������� C++�� ����Ϸ��� ������ �ͼ������� �ʾҴ�.
* vector, queue, priority_queue, struct���� ���̺귯���鿡 �ͼ������� ���θ� �ؾ� �� �� ����.

*/
int main(int argc, char** argv) {
	cin >> T;
	for (test_case = 1; test_case <= T; test_case++) {
		cin >> dump; // ������ �� �� �ִ� ������ Ƚ��
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