#include "helpers_server.h"

std::unordered_map<std::string, bool> users;
std::unordered_map<std::string, bool> resources;
std::vector<std::string> approvals;


void read_users_db(char *users_db_file) {
    std::ifstream users_db(users_db_file);

    if (!users_db.is_open()) {
        std::cout << "Error opening file" << std::endl;
        return;
    }

    int number_of_users;
    users_db >> number_of_users;

    std::string user_id;
    while(std::getline(users_db, user_id)) {
        users[user_id] = true;
    }

    users_db.close();
}

void read_resources_db(char *resources_db_file) {
    std::ifstream resources_db(resources_db_file);

    if (!resources_db.is_open()) {
        std::cout << "Error opening file" << std::endl;
        return;
    }

    int number_of_resources;
    resources_db >> number_of_resources;

    std::string resource_id;
    while(std::getline(resources_db, resource_id)) {
        resources[resource_id] = true;
    }

    resources_db.close();
}

void read_approvals(char *users_approval_responses) {
    std::ifstream users_approval_db(users_approval_responses);
    
    if (!users_approval_db.is_open()) {
        std::cout << "Error opening file" << std::endl;
        return;
    }

    std::string line;
    while(std::getline(users_approval_db, line)) {
        approvals.push_back(line);
    }

    users_approval_db.close();
}

void command_line_arguments_support(int argc, char *argv[]) {
    if (argc < 4) {
        std::cout << "Try to run again with more arguments" << std::endl;
        return;
    }

    char *users_db_file = argv[1];
    char *resources_db_file = argv[2];
    char *users_approval_db_file = argv[3];

    read_users_db(users_db_file);
    read_resources_db(resources_db_file);
    read_approvals(users_approval_db_file);
}