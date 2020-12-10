#!/bin/bash

# The idea here is to ping the host's ssh to check its readiness before running the ansible script.
# This idea is still a WIP, main becuase the source for the ansible_ssh_host_or_ip is yet to be determined.

counter=0;
while ! nc -vz <ansible_ssh_host_tbc> 22; do
  counter=$((counter+1));
  if [ $counter -eq 24 ]; then break; fi;
  sleep 10;
done

ansible-playbook src/builds/vm/playbook/main.yml