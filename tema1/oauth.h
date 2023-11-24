/*
 * It was generated using rpcgen.
 * It was modified in order to add support for command line args.
 */

#ifndef _OAUTH_H_RPCGEN
#define _OAUTH_H_RPCGEN

#include <rpc/rpc.h>


#ifdef __cplusplus
extern "C" {
#endif


struct tokken {
	int approved;
	int ttl;
	char *type;
	char *value;
};
typedef struct tokken tokken;

struct cl_request {
	int user_index;
	char *client_id;
	char *info;
	struct tokken tokken;
};
typedef struct cl_request cl_request;

struct ser_response {
	char *message;
	struct tokken auto_token;
	struct tokken access_token;
	struct tokken refresh_token;
};
typedef struct ser_response ser_response;

#define OAUTH_PROG 0x33445566
#define OAUTH_VERS 1

#if defined(__STDC__) || defined(__cplusplus)
#define request_autorization 1
extern  struct ser_response * request_autorization_1(struct cl_request *, CLIENT *);
extern  struct ser_response * request_autorization_1_svc(struct cl_request *, struct svc_req *);
#define request_approve 2
extern  struct ser_response * request_approve_1(struct cl_request *, CLIENT *);
extern  struct ser_response * request_approve_1_svc(struct cl_request *, struct svc_req *);
#define request_access_token 3
extern  struct ser_response * request_access_token_1(struct cl_request *, CLIENT *);
extern  struct ser_response * request_access_token_1_svc(struct cl_request *, struct svc_req *);
#define validate_delegated_action 4
extern  struct ser_response * validate_delegated_action_1(struct cl_request *, CLIENT *);
extern  struct ser_response * validate_delegated_action_1_svc(struct cl_request *, struct svc_req *);
#define refresh_access_token 5
extern  struct ser_response * refresh_access_token_1(struct cl_request *, CLIENT *);
extern  struct ser_response * refresh_access_token_1_svc(struct cl_request *, struct svc_req *);
extern int oauth_prog_1_freeresult (SVCXPRT *, xdrproc_t, caddr_t);

#else /* K&R C */
#define request_autorization 1
extern  struct ser_response * request_autorization_1();
extern  struct ser_response * request_autorization_1_svc();
#define request_approve 2
extern  struct ser_response * request_approve_1();
extern  struct ser_response * request_approve_1_svc();
#define request_access_token 3
extern  struct ser_response * request_access_token_1();
extern  struct ser_response * request_access_token_1_svc();
#define validate_delegated_action 4
extern  struct ser_response * validate_delegated_action_1();
extern  struct ser_response * validate_delegated_action_1_svc();
#define refresh_access_token 5
extern  struct ser_response * refresh_access_token_1();
extern  struct ser_response * refresh_access_token_1_svc();
extern int oauth_prog_1_freeresult ();
#endif /* K&R C */

/* the xdr functions */

#if defined(__STDC__) || defined(__cplusplus)
extern  bool_t xdr_tokken (XDR *, tokken*);
extern  bool_t xdr_cl_request (XDR *, cl_request*);
extern  bool_t xdr_ser_response (XDR *, ser_response*);

#else /* K&R C */
extern bool_t xdr_tokken ();
extern bool_t xdr_cl_request ();
extern bool_t xdr_ser_response ();

#endif /* K&R C */

#ifdef __cplusplus
}
#endif

#endif /* !_OAUTH_H_RPCGEN */
