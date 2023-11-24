#ifndef HELPERS_CLIENT_H
#define HELPERS_CLIENT_H

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_map>
#include <stdlib.h>
#include <string.h>
#include "oauth.h"

char *string_to_char(std::string str);
struct tokken create_empty_token();
struct tokken create_token(int approved, std::string type,
                            std::string initial_value, int ttl = 0);

#endif // HELPERS_CLIENT_H