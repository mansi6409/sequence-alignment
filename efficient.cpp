#include <iostream>
#include <fstream>
#include <string>

using namespace std;

bool isInteger(const std::string& s) {
    return !s.empty() && std::all_of(s.begin(), s.end(), ::isdigit);
}

void createInput(ifstream& inputFile) {
    string inputArr[2];
    string line;
    string currStr;
    int i = -1;
    int count = 1;
    while (getline(inputFile, line)) {
        if (!isInteger(line)){
            cout << line << endl;
            inputArr[++i] = line;
            currStr = line;
            count = 1;
        }
        else {
            string result;
            for (int j = 0; j < count; j++) {
                result += currStr;
            }
            inputArr[i].insert(stoi(line)+1, result);
            count++;
        }
    }
    for (i=0; i < 3; i++) {
        cout << inputArr[i] << endl;
    }
}

int main() {
    ifstream inputFile("inputData/mockInput.txt");

    if (!inputFile.is_open()) {
        cerr << "Error opening the file" << endl;
        return 1;
    }

    createInput(inputFile);

    inputFile.close();

    return 0;
}