#!/bin/bash

mkdir -p elasticsearch/storage
chown -R 1000:1000 elasticsearch/storage/
mkdir -p logstash/{config,pipeline,logfile}
mkdir -p kibana/config
mkdir -p nginx/{public,data,etc}