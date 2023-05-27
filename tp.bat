
@echo off
setlocal EnableDelayedExpansion

set "protocol=socks4"
set "server=181.78.16.225"
set "port=5678"

curl "http://httpbin.org/ip" --proxy "%protocol%://%server%:%port%"