# HostChecker

Simple CLI tool to check who is hosting a website

## Install

Install using pip:

`pip install hostchecker`

## Usage

Get who is hosting a website:

```console
$ py -m hostchecker www.google.com
www.google.com                           Google LLC                               1.33s
```

Get the hosting service of all your bookmarks *(support only for chrome)*:

```console
$ py -m hostchecker
www.pcgamer.com                          Amazon.com, Inc.                         0.68s
www.hackerrank.com                       Akamai Technologies, Inc.                0.83s
translate.google.it                      Google LLC                               0.65s
www.opengl-tutorial.org                  Fastly                                   2.72s
bitbucket.org                            Amazon.com, Inc.                         0.72s
mosquitto.org                            Bitfolk Ltd                              1.22s
www.haskell.org                          PACKET                                   0.86s
```

Get useful stats for the most popular hosting service:

```console
$ py -m hostchecker --stats
Microsoft Corporation                    09 04.1%
Akamai Technologies, Inc.                15 06.8%
Google LLC                               20 09.1%
Amazon.com, Inc.                         24 10.9%
Cloudflare, Inc.                         24 10.9%
Fastly                                   28 12.7%
```

## License

You can reed it [here](./LICENSE)
