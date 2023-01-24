#include <cstdio>
#include <iostream>
#include <vector>
#include <list>
#include <sstream>
#include <iterator>

using namespace std;

int test_case;
int T = 10;
int N, M;

string amho;
string command;
string answer;
list<string> amhoL;
list<string> commandL;

list<string> split(string input, char delim) {
	list<string> answer;
	stringstream ss(input);
	string temp;

	while (getline(ss, temp, delim)) {
		answer.push_back(temp);
	}
	return answer;
}

list<string> Insert(list<string> input, list<string> temp, string s, int x) {
	auto cursor = input.begin();
	for (int i = 0; i < x; i++) {
		cursor++;
	}
	temp.push_back(s);



	return temp;
}

list<string> Delete(list<string> input, int x, int y) {
	auto cursor = input.begin();
	for (int i = 0; i < x; i++) {
		cursor++;
	}
	for (int i = 0; i < y; i++) {
		input.erase(cursor);
	}

	return input;
}
int main() {
	for (test_case = 1; test_case <= T; ++test_case) {
		amho, command = "", ""; // �ʱ�ȭ
		amhoL.clear();
		commandL.clear();
		cin >> N;
		cin.ignore();
		getline(cin, amho);
		//cin.ignore();
		amhoL = split(amho, ' ');
		// cout << "SIZE " << amhoL.size() << endl;
		cin >> M;
		cin.ignore();
		getline(cin, command);
		//cin.ignore();
		commandL = split(command, ' ');


		while (commandL.empty() == false) { // ������� ���� ������ �ݺ�
			//cout << "NOT EMPTY" << endl;
			string temp = commandL.front();
			if (temp == "I") { // insert�� �ؾ� �ϴ� ��Ȳ�̶�� 
				//cout << "START INSERT" << endl;
				commandL.pop_front();
				int x = stoi(commandL.front()); // �տ��������� ��ġ
				commandL.pop_front();
				int y = stoi(commandL.front()); // �Է��ؾ� �ϴ� ����
				commandL.pop_front();
				cursor = amhoL.begin();

				for (int i = 0; i < x; i++) {
					cursor++;
				}

				list<string> temp;
				for (int i = 0; i < y; i++) {
					string s = commandL.front();
					cout << s;
					temp.push_back(s);
					commandL.pop_front();
				}
				amhoL.splice(cursor, temp);
			}

			if (temp == "D") { // deletd�� �ؾ��ϴ� ��Ȳ�̶��
				commandL.pop_front();
				int x = stoi(commandL.front());
				commandL.pop_front();
				int y = stoi(commandL.front());
				commandL.pop_front();

				amhoL = Delete(amhoL, x, y);
				cout << "SUCCESS DELETE" << endl;
			}

			if (temp == "A") { // Add�� �ؾ� ��
				commandL.pop_front();
				int y = stoi(commandL.front());
				commandL.pop_front();

				for (int i = 0; i < y; i++) {
					string s = commandL.front();
					amhoL.push_back(s);
				}
				cout << "SUCCESS ADD" << endl;

			}
		}
		auto itr = amhoL.begin();
		cout << "#" << test_case << " ";
		for (int i = 0; i < 10; i++, itr++) {
			cout << *itr << " ";
		}
		cout << endl;
	}
	return  0;
}