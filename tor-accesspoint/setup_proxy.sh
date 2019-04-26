sudo su
apt-get update
apt-get upgrade
apt-get install tor privoxy -y
echo "SocksPort 9050
SocksListenAddress 127.0.0.1
Log info file /var/log/tor/notices.log" > /etc/tor/torrc

echo "user-manual /usr/share/doc/privoxy/user-manual
confdir /etc/privoxy
logdir /var/log/privoxy
actionsfile match-all.action # Actions that are applied to all sites and maybe overruled later on.
actionsfile default.action   # Main actions file
actionsfile user.action      # User customizations
filterfile default.filter
filterfile user.filter      # User customizations
debug   1
logfile logfile
listen-address  127.0.0.1:3128
listen-address  [::1]:3128
listen-address  192.168.1.1:3128
toggle  1
enable-remote-toggle  0
enable-remote-http-toggle  0
enable-edit-actions 0
enforce-blocks 0
buffer-limit 4096
enable-proxy-authentication-forwarding 0
forwarded-connect-retries  0
accept-intercepted-requests 0
allow-cgi-request-crunching 0
split-large-forms 0
keep-alive-timeout 5
tolerate-pipelining 1
socket-timeout 300
forward-socks5 / localhost:9050 .
" > /etc/privoxy/config

systemctl enable tor privoxy
systemctl restart tor privoxy
exit
