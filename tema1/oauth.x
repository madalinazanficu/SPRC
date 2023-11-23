struct tokken {
    int approved;
    int ttl;
    string type<>;
    string value<>;
};

struct cl_request {
    int user_index;
    string client_id<>;
    string info<>;
    struct tokken tokken;
};

struct ser_response {
    string message<>;
    struct tokken auto_token;
    struct tokken access_token;
    struct tokken refresh_token;
};

program OAUTH_PROG {
    version OAUTH_VERS {
        struct ser_response request_autorization(struct cl_request) = 1;
        struct ser_response request_approve(struct cl_request) = 2;
        struct ser_response request_access_token(struct cl_request) = 3;
        struct ser_response validate_delegated_action(struct cl_request) = 4;
        struct ser_response refresh_access_token(struct cl_request) = 5;
    } = 1;
} = 0x33445566;