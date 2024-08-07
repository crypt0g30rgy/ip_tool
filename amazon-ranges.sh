#!/usr/bin/env bash

# Define a timestamp function
timestamp=$(date +"%Y-%m-%d_%H-%M-%S")

## -- Download All Ips --

wget https://ip-ranges.amazonaws.com/ip-ranges.json

## -- Extract IPv4 Addresses --

cat ip-ranges.json | jq '.prefixes' | tee -a ipv4.json

## -- Get ec2 ipv4 addresses -- 

jq -r '.[] | select(.service == "EC2") | .ip_prefix' ipv4.json  | tee -a ec2.json

## -- For Comparison --

mv ip-ranges.json $timestamp-ip-ranges.json
