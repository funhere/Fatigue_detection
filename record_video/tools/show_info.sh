#!/bin/bash

ifconfig | grep -A 1 -B 1 inet

tail -f show_info.sh
