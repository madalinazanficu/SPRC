#include "helpers_server.h"


// Initialize the server's database
std::unordered_map<std::string, bool> users;
std::unordered_map<std::string, bool> resources;
std::vector<std::string> approvals;
std::unordered_map<std::string, std::string> access_tokens;
std::unordered_map<std::string, std::string> refresh_tokens;
std::unordered_map<std::string, int> user_ttl;
std::unordered_map<std::string,
                std::unordered_map<std::string, std::string>> token_perm;

int token_availability;

/*
    Based on the index, parse an approval line and save the permissions
    Split each line by ',' and iterate 2 by 2 words to interpret the permissions.
*/
std::string parse_permissions(int index,
                            std::unordered_map<std::string, std::string>& permissions) {

    std::string line = approvals[index];
    std::stringstream ss(line);

    std::vector<std::string> parts;
    while (ss.good()) {
        std::string substr;
        std::getline(ss, substr, ',');
        parts.push_back(substr);
    }
    
    for (int i = 0; i < parts.size(); i += 2) {
        permissions[parts[i]] = parts[i + 1];
        if (parts[i] == "*" && parts[i + 1] == "-") {
            return "DENIED";
        }
    }
    return "PERMITTED";
}


/*
    Read usersIDs.db and save the users id in the database.
*/
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


/*
    Read resources.db and save the resources in the database.
*/
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

/*
    Read usersApproval.db and save the users approval responses
    in the database.
*/

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

/*
    Function called from oauth_svc.cpp to initialize to get input files,
    from command line arguments.
*/
void command_line_arguments_support(int argc, char *argv[]) {
    if (argc < 5) {
        std::cout << "Try to run again with more arguments" << std::endl;
        return;
    }

    char *users_db_file = argv[1];
    char *resources_db_file = argv[2];
    char *users_approval_db_file = argv[3];
    char *token_av = argv[4];

    read_users_db(users_db_file);
    read_resources_db(resources_db_file);
    read_approvals(users_approval_db_file);
    token_availability = atoi(token_av);
    
}
