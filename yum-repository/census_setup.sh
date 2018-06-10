#!/bin/bash

PATH=/usr/bin:/bin
OS_DATA=/etc/os-release
#YUM_VARS=/etc/yum/vars
#DNF_TREE=/etc/dnf
YUM_VARS=/home/smooge/test/yum/vars
DNF_TREE=/home/smooge/test/dnf
PROC_UUID=/proc/sys/kernel/random/uuid
YUM_UUID=/var/lib/yum/uuid


##
## We only accept one command line argument update which will force the script to run update.
UPDATE=0
if [[ $# -gt 0 ]]; then
    if [[ "x$1" == "xupdate" ]]; then
	UPDATE=1
    fi
fi

##
## This function will create the files if they don't exist already
##
function populate_files(){
    if [[ $# -eq 0 ]]; then
	# we were not called correctly
	return
    fi
    local DIR=$1
    if [[ ${UPDATE} -eq 0 ]]; then
	if [[ -d $DIR ]]; then
	    if [[ ! -s ${DIR}/census_os ]]; then
		echo ${ID} > ${DIR}/census_os
	    fi
	    if [[ ! -s ${DIR}/census_variant ]]; then
		echo ${VARIANT_ID} > ${DIR}/census_variant
	    fi
	    if [[ ! -s ${DIR}/census_uuid ]]; then
		echo ${UUID} > ${DIR}/census_uuid
	    fi
	fi
    else
	if [[ -d $DIR ]]; then
	    echo ${ID} > ${DIR}/census_id
	    echo ${VARIANT_ID} > ${DIR}/census_variant
	    echo ${UUID} > ${DIR}/census_uuid
	fi
    fi
}

##
## Make a UUID
## 
function mk_uuid(){
    ## Use an existing uuid if it exists
    if [[ -s ${YUM_UUID} ]]; then
	UUID=$( cat ${YUM_UUID} )
    elif  [[ -f ${PROC_UUID} ]]; then
	UUID=$( cat ${PROC_UUID} )
    else 
	UUID="ffffffff-ffff-ffff-ffff-ffffffffffff"
    fi
}


## Check to see if there is an OS release file
## if there is then source it and set up the census directories
##
if [[ -f ${OS_DATA} ]]; then
    . ${OS_DATA}
    if [ $? -ne 0 ]; then
	# something went wrong and we should stop
	echo "Unable to parse ${OS_DATA}"
	exit
    fi
    ## Things we want
    ## $ID
    ## $VERSION_ID
    ## $VARIANT_ID
    if [[ "x${VARIANT_ID}" == "x" ]]; then
	VARIANT_ID=none
    fi
else
    ID=unknown
    VARIANT_ID=none
fi

mk_uuid

## Determine if we have yum variables we need to populate

if [[ -d ${YUM_VARS} ]]; then
    populate_files ${YUM_VARS}
fi

## DNF does not create a vars directory by default. We need to do so.

if [[ -d ${DNF_TREE} ]]; then
    if [[ ! -d ${DNF_TREE}/vars ]]; then
	mkdir -p ${DNF_TREE}/vars
    fi
    populate_files ${DNF_TREE}/vars
fi
