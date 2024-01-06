#include <iostream>
#include <vector>
#include <queue>
#include <cmath>
#include <tuple>
using namespace std;

vector <int> DY = { -1,-1,0,0,1,1 };
vector <int> DX = { -1,0,-1,1,0,1 };



pair<int, int> getXY(int n) {
	int diff = 1;
	while (n > 0) {
		int temp = n - diff;
		if (temp > 0) {
			diff++;
			n = temp;
		}
		else {
			int y = diff;
			int x = n;
			return make_pair(y, x);
		}
	}
	// Handle invalid case if needed
	return make_pair(-1, -1);
}

int min_dist(int s, int e) {
	pair<int, int> sxy = getXY(s);
	pair<int, int> exy = getXY(e);
	int ey = 0; int ex = 0; int sy = 0; int sx = 0;
	ey = exy.first; ex = exy.second;
	sy = sxy.first; sx= sxy.second;
	// cout << "End (Y, X) :" << ey << " " << ex << endl;
	// cout << "Start (Y, X) :" << sy << " " << sx << endl;
	int mv_y = ey - sy;
	if (ex == sx) {
		return mv_y;
	}
	else if (ex > sx) {
		int diff_x = ex - sx;
		if (diff_x > mv_y) {
			return diff_x;
		}
		else {
			return mv_y;
		}
	}
	else {
		int diff_x = sx - ex;
		return mv_y + diff_x;
	}

}
int main(int argc, char** argv) {
	int test_case;
	int T;
	int s, e; // 출발, 도착 
	int temp;

	cin >> T;

	for (test_case = 1; test_case <= T; ++test_case) {
		cin >> s >> e;
		if (s > e) { // 무조건 출발 노드가 더 작도록 변경 (굳이 안해도 될것 같긴 한데 그래도)
			temp = s;
			s = e;
			e = temp;
		}
		// int answer = bfs(s, e);
		int answer = min_dist(s, e);
		cout << "#" << test_case << " " << answer << endl;

	}
	return 0;
}