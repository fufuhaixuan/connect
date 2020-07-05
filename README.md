# connect
 Terminal SSH connection management in python2.7
 
# usage
Set a new config: connect -cmd set -n myname -host username@host[:port] -pwd mypassword
Delete a config:  connect -cmd delete -n myname
Update a config:  connect -cmd update -n myname -update password:newpassword

# how to use
> python connect.py
Select a number to connect:
[0] name1         ip1
[1] name2         ip2
[e] exit

Enter a number to connect to the corresponding IP

