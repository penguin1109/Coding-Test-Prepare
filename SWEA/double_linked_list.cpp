#define MAX_NODE 10000

struct Node {
	int data;
	Node* prev;
	Node* next;
};

Node node[MAX_NODE];
int nodeCnt;
Node* head;

Node* getNode(int data) {
	node[nodeCnt].data = data;
	node[nodeCnt].prev = nullptr;
	node[nodeCnt].next = nullptr;
	return &node[nodeCnt++];
}

void init() // ÃÊ±âÈ­
{
	nodeCnt = 0;
	head = new Node;
	head->data = -1;
	head->prev = nullptr;
	head->next = nullptr;
}

void addNode2Head(int data)
{
	Node* new_node = new Node;
	new_node->data = data;
	Node* next = new Node;
	next = head->next;
	if (next == nullptr) {
		head->next = new_node;
		new_node->prev = head;
		new_node->next = head;
		head->prev = new_node;
	}
	else {
		next->prev = new_node;
		new_node->next = next;
		head->next = new_node;
		new_node->prev = head;
	}

	nodeCnt += 1;

}

void addNode2Tail(int data)
{
	Node* new_node = new Node;
	new_node->data = data;
	Node* tail = new Node;
	tail = head->prev;

	tail->next = new_node;
	new_node->prev = tail;
	new_node->next = head;
	head->prev = new_node;

	nodeCnt += 1;
}

void addNode2Num(int data, int num)
{
	Node* new_node = new Node;
	new_node->data = data;
	Node* temp = new Node;
	temp = head;
	for (int i = 0; i < num - 1; i++) {
		temp = temp->next;
	}
	Node* next = new Node;
	next = temp->next;
	temp->next = new_node;
	new_node->prev = temp;
	next->prev = new_node;
	new_node->next = next;
	nodeCnt += 1;
}

int findNode(int data)
{
	Node* temp = new Node;
	temp = head;
	for (int i = 1; i <= nodeCnt; i++) {
		temp = temp->next;
		if (temp->data == data) {
			return i;
		}
	}
}

void removeNode(int data)
{
	Node* temp = new Node;
	temp = head;
	while (temp->next != head) {
		temp = temp->next;
		int d = temp->data;
		if (d == data) {
			Node* rm = new Node;
			rm = temp;
			Node* prev = new Node;
			prev = temp->prev;
			Node* next = new Node;
			next = temp->next;
			prev->next = next;
			next->prev = prev;
			nodeCnt -= 1;
		}
	}
}

int getList(int output[MAX_NODE])
{
	int cnt = 0;
	Node* temp = new Node;
	temp = head;
	while (temp->next != head) {
		temp = temp->next;
		output[cnt] = temp->data;
		cnt += 1;
	}
	return cnt;
}

int getReversedList(int output[MAX_NODE])
{
	int cnt = 0;
	Node* temp = new Node;
	temp = head;
	while (temp->prev != head) {
		temp = temp->prev;
		output[cnt] = temp->data;
		cnt += 1;
	}
	return cnt;
}