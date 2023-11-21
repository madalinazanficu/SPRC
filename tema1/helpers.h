#ifndef HELPERS_H
#define HELPERS_H

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_map>

// Saved users id read from usersIDs.db: entry - (user_id, active=true) 
extern std::unordered_map<std::string, bool> users;

// Server resources read from resources.db: entry - (resource_id, active=true)
extern std::unordered_map<std::string, bool> resources;

// Users approval responses read from usersApproval.db
extern std::vector<std::string> approvals;



// Server pre-configuration functions
void command_line_arguments_support(int argc, char *argv[]);
void read_users_db(char *users_db_file);
void read_resources_db(char *resources_db_file);
void read_approvals(char *users_approval_responses);


#endif // HELPERS_H