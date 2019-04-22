#!/bin/bash

# https://github.com/qbittorrent/qBittorrent/wiki/Web-API-Documentation 
url="https://192.168.2.2:8080"
usr='admin'
pw='adminadmin'

cookie=""

function login(){
    cookie=$(curl "$url/api/v2/auth/login" --data "username=$usr&password=$pw" --compressed -i awk '/Set-Cookie/{print $2}')
}

function add_by_link(){
    urls=$(printf '%s\n' "$@")
    curl -k "$url/api/v2/torrents/add" -b "$cookie" -F"urls=$urls"
}

function add_by_torrent_file(){
    torrents=$(printf ' -F torrents=@"%s";type=application/x-bittorrent' "$@")
    echo $torrents
    curl -k "$url/api/v2/torrents/add" -b "$cookie" $torrents
}

login

if [ -z "${1##*http*}" ]
then
    add_by_link "$@"
else
    add_by_torrent_file "$@"
fi

# add_link "https://x.cc/download.php?id=1203[5-7]"
# add_by_torrent_file /tmp/*.txt
