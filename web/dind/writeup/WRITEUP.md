# Docker-ception Writeup

We're looking at an unsanitized input allowed for RCE on the inner docker container. After realizing you can run code on the inner container, we need to find a way to escape it/ read the outer docker container.

The intended path is realizing you can view running docker daemon processes from the lower container. If you have access to docker daemon, you can try mounting a bind mount of the upper container. This lets you read the file system (but wont make any persist changes to it).


8.8.8.8; docker run --rm -v /:/mnt alpine sh -c "cat /mnt/flag/flag.txt";
