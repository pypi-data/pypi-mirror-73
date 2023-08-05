#!/usr/bin/env python
# coding: utf-8
# author: Frank YCJ
# email: 1320259466@qq.com
import hashlib

def get_md5(data,salt="",rounds=1):
    md5 = hashlib.md5()
    tag=0
    while tag<rounds:
        data = data + salt
        md5.update(data)
        data=md5.hexdigest()
        tag=tag+1

    return data

def get_sha1(data):
    sha1=hashlib.sha1()
    sha1.update(data)
    return sha1.hexdigest()

def get_sha224(data):
    sha1=hashlib.sha224()
    sha1.update(data)
    return sha1.hexdigest()

def get_sha256(data):
    sha1=hashlib.sha256()
    sha1.update(data)
    return sha1.hexdigest()

def get_sha384(data):
    sha1=hashlib.sha384()
    sha1.update(data)
    return sha1.hexdigest()


def get_sha512(data):
    sha1=hashlib.sha512()
    sha1.update(data)
    return sha1.hexdigest()


