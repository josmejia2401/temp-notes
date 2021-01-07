package main

import (
    "net/url"
    "os"
)

var environment = UtilGetEnvironment()

var ALLOW_HOST = map[string]string{
    "soursop-dev.blogspot.com": UtilHostTarget(),
}

func UtilGetEnvironment() string {
    return os.Getenv("ENVIRONMENT")
}

func UtilHostTarget() string {
    var URL = "soursop-dev.blogspot.com"
    var scheme = "https"
    url := url.URL{
        Scheme: scheme,
        Host:   URL,
    }
    return url.String()
}