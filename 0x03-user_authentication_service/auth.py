#!/usr/bin/env python3
"""A module for authentication-related routines.
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    ''' Hash a password with bcrypt
    '''
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed
