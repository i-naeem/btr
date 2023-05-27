
@echo off
setlocal EnableDelayedExpansion

set "protocol=socks5"
set "server=185.199.229.156"
set "port=7492"

curl "http://httpbin.org/ip" --proxy "%protocol%://%server%:%port%"