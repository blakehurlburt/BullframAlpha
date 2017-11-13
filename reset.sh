ps aux | grep -v grep | grep python | awk '{print "kill -9 "$2}' | bash
