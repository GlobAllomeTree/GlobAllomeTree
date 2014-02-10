#Must run this line on start up source server/configure_vagrant_shell.sh 
dock_attach() {
  sudo lxc-attach -n `sudo docker inspect $1 | grep '"ID"' | sed 's/[^0-9a-z]//g'` /bin/bash
}
alias dock-attach=dock_attach