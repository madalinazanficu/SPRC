#include "helpers.h"

void read_clients_id(int test_number) {

}




void read_clients_input() {
    std::ifstream clients("tests/tests/test1/client.in");
    std::cout << "In read clients ids\n";

    std::string line;
    while(std::getline(clients, line)) {
        std::cout << line << std::endl;

        std::stringstream ss(line);
        std::vector<std::string> command_parts;
        while(ss.good()) {
            std::string substr;
            std::getline(ss, substr, ',');
            command_parts.push_back(substr);
        }

    }

    clients.close();
}