struct token {
    string type<>;
};

struct request {
    string client_id<>;
    struct token token;
};

struct response {
    string message<>;
    struct token auto_token;
    struct token access_token;
    struct token refresh_token;
};

program OAUTH_PROG {
    version OAUTH_VERS {
        struct response request_autorization(struct request) = 1;
        struct response request_approve(struct request) = 2;
        struct response request_access_token(struct request) = 3;
        struct response validate_delegated_action(struct request) = 4;
    } = 1;
} = 0x33445566;