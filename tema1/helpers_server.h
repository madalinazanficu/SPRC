#ifndef HELPERS_SERVER_H
#define HELPERS_SERVER_H

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_map>
#include <stdlib.h>
#include <string.h>
#include <string>


/* 
    Server's database
*/

// Saved users id read from usersIDs.db: entry - (user_id, active=true) 
extern std::unordered_map<std::string, bool> users;

// Server resources read from resources.db: entry - (resource_id, active=true)
extern std::unordered_map<std::string, bool> resources;

// Users approval responses read from usersApproval.db
extern std::vector<std::string> approvals;

// Token availability is passed as a command line argument
extern int token_availability;


// Each user will have a unique access token in the database
extern std::unordered_map<std::string, std::string> access_tokens;

// Each user may have a refresh token in the database
extern std::unordered_map<std::string, std::string> refresh_tokens;

// Each user will have a TTL for the access token
extern std::unordered_map<std::string, int> user_ttl;

/* 
    Each token will have a list of permissions for each resource
    ex: token1 --> resource1 --> RM 
               --> resource2 --> RIMD
*/
extern std::unordered_map<std::string,
                    std::unordered_map<std::string, std::string>> token_perm;



// Server pre-configuration functions
void command_line_arguments_support(int argc, char *argv[]);
void read_users_db(char *users_db_file);
void read_resources_db(char *resources_db_file);
void read_approvals(char *users_approval_responses);
std::string parse_permissions(int index,
                    std::unordered_map<std::string, std::string>& permissions);


#endif // HELPERS_SERVER_H