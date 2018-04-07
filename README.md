# oniongen
Deep Web .onion URL Generator

## About
**oniongen** is a small cli tool that generates and validates .onion urls.

## Installation
You can get the lastest version by clonning this repository:
```shell
git clone https://github.com/k11dd00/oniongen
cd oniongen && sudo pip install -r requirements.txt
```

## Usage
```shell
python oniongen.py <options> url
```
The oniongen cli takes one positional argument(url) that represents an url:
```shell
python oniongen.py --validate "http://3g2upl4pq6kufc4m.onion/"
```

See the options overview:

Short opt | Long opt | Default | Required | Description
--------- | -------- | ------- | -------- | -----------
-h        | --help        | None      | No  | shows the help usage
-c        | --count       | 100       | Yes | the number of urls to generate
-p        | --prefix      | None      | No  | the url prefix
-s        | --suffix      | None      | No  | the url suffix
-w        | --workers     | 100       | Yes | the number of url validation workers
-g        | --generate    | True      | No  | generates random .onion urls
-i        | --input       | None      | No  | the url list file
-o        | --output      | None      | No  | the output file
N/A       | --protocol    | http      | No  | the protocol(http or https)
N/A       | --tld         | .onion    | No  | the top level domain
N/A       | --validate    | False     | No  | validates the given url
N/A       | --discover    | False     | No  | enables the discover mode
N/A       | --proxy-ip    | 127.0.0.1 | Yes | the Tor proxy ip
N/A       | --proxy-port  | 9050      | Yes | the Tor proxy port
N/A       | --dry-run     | False     | No  | disables proxy and url validation
N/A       | --version     | None      | No  | shows the current version

## Validating .onion URLs

```shell
python oniongen.py --validate "http://3g2upl4pq6kufc4m.onion/"

             <ONIONGEN>
    Deep Web .onion URL Generator

                        [k1dd00]
                          v1.0.0
    
[+] Setting up proxy config
[+] Proxy IP:   127.0.0.1
[+] Proxy PORT: 9050
[+] Checking Tor Status
[+] Tor Status: READY
[+] Checking IP Address
[+] IP: 51.15.81.222
[+] Running HTTP status check in 1 url(s)
[+] Be patient, this may take a looooong time...
[+] Found: DuckDuckGo Search Engine | http://3g2upl4pq6kufc4m.onion/
[+] Found 1 of 1 urls
```
### Validating .onion URLs Using Files as Input/Output
```shell
python oniongen.py --validate -i urls.txt -o active_urls.txt

             <ONIONGEN>
    Deep Web .onion URL Generator

                        [k1dd00]
                          v1.0.0
    
[+] Setting up proxy config
[+] Proxy IP:   127.0.0.1
[+] Proxy PORT: 9050
[+] Checking Tor Status
[+] Tor Status: READY
[+] Checking IP Address
[+] IP: 51.15.81.222
[+] Running HTTP status check in 3 url(s)
[+] Be patient, this may take a looooong time...
[+] Found: TORCH: Tor Search! | http://xmh57jrzrnw6insl.onion
[+] Found: DuckDuckGo Search Engine | https://3g2upl4pq6kufc4m.onion/
[+] Found: DuckDuckGo Search Engine | http://3g2upl4pq6kufc4m.onion/
[+] Found 3 of 3 urls
```

## Generating Random .onion URLs

```shell
python oniongen.py -g
```

To change the default parameters:

```shell
python oniongen.py -g -c 10 -p parasite -s abc -w 10
```

## The "discover" mode

The discover mode keeps the script running until it finds the given number of urls.
```shell
python oniongen.py --discover -c 10
```

## Piped Input

You can pipe a list of urls to be validated:
```shell
cat urls.txt | python oniongen.py --validate
```

## Piped Output

The output can also be piped:
```shell
cat urls.txt | python oniongen.py --validate > active_urls.txt
```

## License
This is an open-source software licensed under the [MIT license](https://opensource.org/licenses/MIT).
