#define MAX_NODE 10000
struct Node {
	int data;
	Node* next;
};

Node node[MAX_NODE];
int nodeCnt;
Node* head;

Node* getNode(int data) {
	node[nodeCnt].data = data;
	node[nodeCnt].next = nullptr;
	return &node[nodeCnt++];
}

void init() // 초기화
{
	head = new Node;
	head->data = -1; // head에 dummy값 넣기
	head->next = nullptr;
	nodeCnt = 0;
}

void addNode2Head(int data) // 맨 앞에 노드 추가
{
	Node* new_node = new Node;
	new_node->data = data;
	new_node->next = head->next;
	head->next = new_node;

	nodeCnt += 1;

}

void addNode2Tail(int data) // 맨 뒤에 노드 추가
{
	Node* new_node = new Node;
	new_node->data = data;
	new_node->next = nullptr;
	Node* move = head;
	while (move->next != nullptr) {
		move = move->next;
	}
	move->next = new_node;
	nodeCnt += 1;
}

void addNode2Num(int data, int num) // 지정된 순서에 노드 추가
{
	Node* new_node = new Node;
	new_node->data = data;
	Node* move = head;
	for (int i = 0; i < num - 1; i++) {
		move = move->next;
	}
	Node* temp = move->next;
	move->next = new_node;
	new_node->next = temp;
	nodeCnt += 1;
}


void removeNode(int data) // 주어진 data 값을 가진 노드 삭제
{
	int i = 0;
	Node* prev = new Node;
	Node* next = new Node;
	prev = head;
	next = head->next;
	while (i < nodeCnt) {
		int n = next->data;
		if (n == data) {
			Node* temp = new Node;
			temp = next->next;
			prev->next = temp;
			nodeCnt -= 1;
		}
		prev = next;
		next = next->next;
		i += 1;
	}
}

//output[] 배열에 리스트 노드의 data를 차례로 넣고, 총 노드 개수 리턴
int getList(int output[MAX_NODE])
{
	Node* temp = head;
	int i = 0;
	while ((temp->next) != nullptr) {
		Node* next = temp->next;
		output[i] = next->data;
		temp = temp->next;
		i += 1;
	}
	return i;
}