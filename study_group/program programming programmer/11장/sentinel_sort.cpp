

#include <iostream>
#include <vector>
#include <algorithm> // swap 함수 사용

using namespace std;

void custom_sort(vector<int>& x, int l, int u) {
    int t = x[l];
    int m = u + 1;
    int i = m;

    do {
        while (x[--i] < t); // 조건 만족할 때까지 감소
        cout<<"m:"<<m-1<<" swap with "<< "i:" <<i<<endl;
        swap(x[--m], x[i]); // 값 교환
    } while (i != l);
}

int main() {
    vector<int> arr = {2, 1, 4}; // 테스트할 배열
    int l = 0;   // 배열 시작 인덱스
    int u = arr.size() - 1; // 배열 끝 인덱스

    cout << "Before sorting: ";
    for (int num : arr) cout << num << " ";
    cout << endl;

    custom_sort(arr, l, u);

    cout << "After sorting: ";
    for (int num : arr) cout << num << " ";
    cout << endl;

    return 0;
}
