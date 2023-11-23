CFLAGS = -g -I/usr/include/tirpc

build:
	g++ -o client client.cpp helpers_client.cpp oauth_clnt.c oauth_xdr.c -lnsl -ltirpc $(CFLAGS)
	g++ -o server server.cpp helpers_server.cpp oauth_svc.c oauth_xdr.c -lnsl -ltirpc $(CFLAGS)

rpc-gen:
	rpcgen -aC oauth.x

clean:
	rm -f server client *.o
	
clean-up:
	rm -f oauth_clnt.c oauth_xdr.c oauth_svc.c oauth_xdr.c server client *.o oauth_client.c oauth_server.c oauth.h Makefile.oauth

rename:
	mv oauth_client.c client.cpp
	mv oauth_server.c server.cpp

run-client:
	./client localhost /home/madalina/SPRC/tema1/tests/test1/client.in

run-server:
	./server /home/madalina/SPRC/tema1/tests/test1/userIDs.db /home/madalina/SPRC/tema1/tests/test1/resources.db /home/madalina/SPRC/tema1/tests/test1/approvals.db 3