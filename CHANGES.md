0.2.2 (2015-11-03)
--------------------
- Changed CLI interface from click to plac


0.2.1 (2015-11-03)
--------------------
- Solved the issue of dependencies not installing.

- Added support for dameon processes


0.2.0 (2015-11-01)
-------------------
- Switched to class based clients, servers, sockets and even inet services

- Proxys can either be forked on a server's process, on inet's process or on
their own using the `inetproxy` command

- Inet server can now be started using inetserver command, as well as programmatically(
hope I spelt this right)

- Registeration is now purely registeration. Nothing is generated. This is a major
change as servers will now decide what their addresses(frontend and backend will be)
before registeration.

- Server now supports routing on the same worker.

- Server makes use of workers more obvious with the `spawnworkers` method. In fact
the server only starts when you spawn at least on worker(you might need `loopforever` too)

- Removed magic accessors from _Message objects. Accessing meta, data and raw is now
done using properties

- Constants have been totally removed

- `InetClient` now connects both server(`RoutableServer`) and `Client` to the inetserver
, they no longer talk directly to it.

- Addresses registered are actually permanent. They are stored by inet server.

- Every server uses a proxy, including inetserver itself. But `InetClient` has unregister method
in case you really need to delete the record(This means a trip to inet, which we try to prevent
with `InetClient`'s cache

0.1.2 (2015-10-26)
--------------------
- Added decorator support for creating servers

0.1.1 (2015-10-26)
--------------------
- Modularized the package

- Added retry support with sockets' `create_reliable_req_socket` and 
`reliably_recv_req`