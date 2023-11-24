
/* 
    Generic token structure
    - approved = true (when the server signs the autorization token)
               = false (any other cases)

    - ttl = the number of remaining operations that can be performed
    - type = used to identify token type: autorization / access / refresh
    - value = the effectiv token generated using generate_access_token function
*/
struct tokken {
    int approved;
    int ttl;
    string type<>;
    string value<>;
};


/*
    Generic request structure
    - user_index = used to identify the current approval from the user
    - client_id
    - info = contains additional information about the request
            (ex: operations and resource)
    - token = some requests need to pass a specific token to the server
            (ex: autorization token, in order to be signed)
*/

struct cl_request {
    int user_index;
    string client_id<>;
    string info<>;
    struct tokken tokken;
};


/*
    Generic response structure
    - message returned from server
    - different tokens returned by server depending on the request made by client
*/
struct ser_response {
    string message<>;
    struct tokken auto_token;
    struct tokken access_token;
    struct tokken refresh_token;
};


/*
    1. request_autorization
        - Operation meant to check the existance of a client in server database.
        - Returns a response containing USER_NOT_FOUND / USER_FOUND
        and the autorization

    2. request approve 
        - The server will read permissions from the final users and approve
        the previous autorization or not.
        - Returns a response containing the autorization token (un)signed.

    3. request_access_token
        - The client is tested if it's eligible for accesing resources.
        - In case autorization token is not signed -> permission denied
        - Otherwise, an access token will be assigned to the current client,
        and optional a refresh token.

    4. validate_delegated_action
        - The server check mutiple conditions to see if the client
        can perform an operation on a resource. 
        ex: - access_token is valid
            - the client has permissions to R/W/E/M/I/D
        - Returns a response containing error/success message.
        
    5. refresh_access_token
        - The server can generate a new access token based on a refresh token,
        in case the client is eligible.
        - Returns a response containing a new access token and a new refresh token.

*/
program OAUTH_PROG {
    version OAUTH_VERS {
        struct ser_response request_autorization(struct cl_request) = 1;
        struct ser_response request_approve(struct cl_request) = 2;
        struct ser_response request_access_token(struct cl_request) = 3;
        struct ser_response validate_delegated_action(struct cl_request) = 4;
        struct ser_response refresh_access_token(struct cl_request) = 5;
    } = 1;
} = 0x33445566;