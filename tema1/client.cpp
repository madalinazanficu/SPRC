/*
 * This is sample code generated by rpcgen.
 * These are only templates and you can use them
 * as a guideline for developing your own functions.
 */

#include "oauth.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_map>
#include <stdlib.h>
#include <string.h>

/* Based on the input, the client can regenerate the access token or not*/
std::unordered_map<std::string, bool> user_refresh;

/* Each user may have only one access token associated */
std::unordered_map<std::string, std::string> access_tok;

/* Each user may have a refresh token associated */
std::unordered_map<std::string, std::string> refresh_tok;

/* Each user has associated an avialablity for his current access token */
std::unordered_map<std::string, int> user_ttl;

/* Each user which perform a REQUEST will have associated a users_idx */
std::unordered_map<std::string, int> users_idx;
int user_index = 0;

char *string_to_char(std::string str) {
	char *cstr = (char *)calloc(str.length() + 1, sizeof(char));
	strcpy(cstr, str.c_str());
	return cstr;
}

struct tokken create_empty_token() {
	struct tokken new_token;
	new_token.approved = 0;
	new_token.type = string_to_char("Empty token");
	new_token.value = string_to_char("");
	new_token.ttl = 0;
	return new_token;
}

struct tokken create_token(int approved, std::string type,
							std::string initial_value, int ttl = 0) {

	struct tokken new_token;
	new_token.approved = approved;
	new_token.type = string_to_char(type);
	new_token.value = string_to_char(initial_value);
	new_token.ttl = ttl;

	return new_token;
}

/* 
	Responsible for requesting autorization from the server.
	The client saves the autorization token received from the server.
	return message: USER_NOT_FOUND / USER_FOUND
*/
std::string request_autorization_fun(CLIENT *clnt, std::string user_id,
										struct tokken &auto_token) {

	struct cl_request  request_autorization_1_arg;
	struct ser_response  *result_1;

	request_autorization_1_arg.client_id = string_to_char(user_id);
	request_autorization_1_arg.tokken = create_empty_token();
	request_autorization_1_arg.info = string_to_char("");

	result_1 = request_autorization_1(&request_autorization_1_arg, clnt);
	if (result_1 == (struct ser_response *) NULL) {
		clnt_perror (clnt, "call failed");
	}

	auto_token = result_1->auto_token;

	return result_1->message;
}


/*
	Responsible for requesting user approval from the server.
	The approval is generated based on the user_index in FIFO order.
*/
void request_user_approvall(CLIENT *clnt, std::string user_id,
								struct tokken &auto_token) {


	struct ser_response  *result_2;
	struct cl_request  request_approve_1_arg;

	request_approve_1_arg.client_id = string_to_char(user_id);
	request_approve_1_arg.tokken = auto_token;
	request_approve_1_arg.info = string_to_char("");
	request_approve_1_arg.user_index = user_index;

	result_2 = request_approve_1(&request_approve_1_arg, clnt);
	if (result_2 == (struct ser_response *) NULL) {
		clnt_perror (clnt, "call failed");
	}

	// A new user received a set of permissions
	users_idx[user_id] = user_index;
	user_index++;

	// The server may have changed the auto_token
	auto_token = result_2->auto_token;
}


/*
	Responsible for requesting access token and refresh token from the server.
	The access token is generated based on the signed auto_token.
	The refresh token is optional.
*/
void request_access(CLIENT *clnt, std::string user_id,
						struct tokken auto_token) {
	struct ser_response  *result_3;
	struct cl_request  request_access_token_1_arg;

	request_access_token_1_arg.client_id = string_to_char(user_id);
	request_access_token_1_arg.tokken = auto_token;
	request_access_token_1_arg.user_index = users_idx[user_id];

	// Check if the user has auto_refresh enabled
	if (user_refresh[user_id] == true) {
		request_access_token_1_arg.info = string_to_char("REFRESH");
	} else {
		request_access_token_1_arg.info = string_to_char("");
	}

	result_3 = request_access_token_1(&request_access_token_1_arg, clnt);
	if (result_3 == (struct ser_response *) NULL) {
		clnt_perror (clnt, "call failed");
	}

	// In this case, the client was not approved
	if (std::string(result_3->message) == "REQUEST_DENIED") {
		std::cout << result_3->message << std::endl;
		return;
	}

	// Print the all tokens generated
	std::string out_val = result_3->auto_token.value + std::string(" -> ") 
							+ result_3->access_token.value;

	if (std::string(result_3->refresh_token.value) != "") {
		out_val += "," + std::string(result_3->refresh_token.value);
	}
	std::cout << out_val << std::endl;

	// Store tokens locally
	access_tok[user_id] = result_3->access_token.value;
	refresh_tok[user_id] = result_3->refresh_token.value;
	user_ttl[user_id] = result_3->access_token.ttl;
}


// The client want to execute a command with the access token to a resource
void validate_delegated_action_fun(CLIENT *clnt, std::string client_id,
								std::string command, std::string resource) {

	std::string access_token = access_tok[client_id];
	int ttl = user_ttl[client_id];

	struct cl_request  delegated_action_1_arg;
	struct ser_response  *result_4;

	// Sever's input (client_id, access_token, command, resource)
	delegated_action_1_arg.client_id = string_to_char(client_id);
	delegated_action_1_arg.tokken = create_token(0, "access", access_token , ttl);
	delegated_action_1_arg.info = string_to_char(command + "," + resource);

	result_4 = validate_delegated_action_1(&delegated_action_1_arg, clnt);
	if (result_4 == (struct ser_response *) NULL) {
		clnt_perror (clnt, "call failed");
	}

	std::cout << result_4->message << std::endl;
}

void process_request_cmd(CLIENT *clnt, std::string client_id,
							std::string auto_refresh) {


	// Check if the current user have auto_refresh enabled
	if (auto_refresh == "1") {
		user_refresh[client_id] = true;
	} else {
		user_refresh[client_id] = false;
	}

	// Step1 : request autorization
	struct tokken auto_token = create_empty_token();

	std::string message = request_autorization_fun(clnt, client_id, auto_token);
	if (message == "USER_NOT_FOUND") {
		std::cout << message << std::endl;
		return;
	}

	// Step2: request user approval
	request_user_approvall(clnt, client_id, auto_token);


	// Step3: request access token and refresh token
	request_access(clnt, client_id, auto_token);
}


std::string refresh_token_fun(CLIENT *clnt, std::string client_id,
							std::string command, std::string resource) {

	std::string access_token = access_tok[client_id];
	std::string refresh_token = refresh_tok[client_id];

	struct ser_response  *result_5;
	struct cl_request  refresh_access_token_1_arg;
	struct tokken refresh = create_token(0, "refresh_token", refresh_token, 0);

	// The request is made with the refresh token
	refresh_access_token_1_arg.client_id = string_to_char(client_id);
	refresh_access_token_1_arg.tokken = refresh;
	refresh_access_token_1_arg.info = string_to_char(command + "," + resource);

	result_5 = refresh_access_token_1(&refresh_access_token_1_arg, clnt);
	if (result_5 == (struct ser_response *) NULL) {
		clnt_perror (clnt, "call failed");
	}

	// Error message
	if (std::string(result_5->message) != "TOKEN_REFRESHED") {
		return result_5->message;
	}

	// Store the access, refresh tokens and token availability
	access_tok[client_id] = result_5->access_token.value;
	refresh_tok[client_id] = result_5->refresh_token.value;
	user_ttl[client_id] = result_5->access_token.ttl;
	return result_5->message;
}


void process_other_cmd(CLIENT *clnt, std::string client_id,
						std::string command, std::string resource) {

	std::string access_token = access_tok[client_id];
	std::string refresh_token = refresh_tok[client_id];
	int ttl = user_ttl[client_id];

	// Check if the access token is still valid
	std::string message = refresh_token_fun(clnt, client_id, command, resource);
	if (message == "PERMISSION_DENIED" || message == "TOKEN_EXPIRED") {
		std::cout << message << std::endl;
		return;
	}

	// The access token is still valid, so the client can execute the command
	validate_delegated_action_fun(clnt, client_id, command, resource);
}


int main (int argc, char *argv[])
{
	char *host;
	if (argc < 3) {
		printf ("usage: %s server_host\n", argv[0]);
		exit (1);
	}

	host = argv[1];
	CLIENT *clnt = clnt_create (host, OAUTH_PROG, OAUTH_VERS, "udp");
	if (clnt == NULL) {
		clnt_pcreateerror (host);
		exit (1);
	}

	char *client_file;
	client_file = argv[2];

	// Read from client file
	std::ifstream clients(client_file);
	std::string command;
	while(std::getline(clients, command)) {
		std::stringstream ss(command);
		std::vector<std::string> command_parts;
		while(ss.good()) {
			std::string substr;
			std::getline(ss, substr, ',');
			command_parts.push_back(substr);
		}

		if (command_parts[1] == "REQUEST") {
			process_request_cmd(clnt, command_parts[0], command_parts[2]);
		} else {
			process_other_cmd(clnt, command_parts[0], command_parts[1], command_parts[2]);
		}
	}

	clnt_destroy (clnt);
	exit (0);
}