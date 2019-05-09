"""
Add a permision system to sysObjects
sysobjects have a permissions entry in tags by default
    all methods allowed by default, must be blocked by uni, obj
        can also be used as a whitelist
    struct
        permissions: {"<methodName>": "<blocked, unblocked, default>", ...}
uni also have permissions that apply to all objects in a uni
    allow by default
    struct
        {"<methodName>": "<blocked, unblocked, default>", ...}
    where this will go idk
CGE has to enforce this by checking if it can do it
    iterate though opList
    or
    handle at attempt run
"""