[![pipeline status](https://gitlab.com/0bs1d1an/sr2t/badges/master/pipeline.svg)](https://gitlab.com/0bs1d1an/sr2t/commits/master)

# Scanning reports to tabular (sr2t)

This tool takes a scanning tool's output file, and converts it to a tabular format (CSV, XLSX, or text table).
This tool can process output from the following tools:

1. Nmap (XML);
2. Nessus (XML);
3. Nikto (XML);
4. Dirble (XML);
5. Testssl (JSON);
6. Fortify (FPR).

## Rationale

This tool can offer a human-readable, tabular format which you can tie to any observations you have drafted in your report.
Why?
Because then your reviewers can tell that you, the pentester, investigated all found open ports, and looked at all scanning reports.

## Dependencies

1. argparse (dev-python/argparse);
2. prettytable (dev-python/prettytable);
3. python (dev-lang/python);
4. xlsxwriter (dev-python/xlsxwriter).

## Install

Using Pip:

`pip install --user sr2t-0bs1d1an`

Using setup.py:

`python setup.py install`

## Usage

You can use sr2t in two ways:

* When installed as package, call the installed script: `sr2t --help`.
* When Git cloned, call the package directly from the root of the Git
repository: `python -m sr2t --help`

```
$ sr2t --help
usage: sr2t [-h] [--nessus NESSUS [NESSUS ...]] [--nmap NMAP [NMAP ...]]
            [--nikto NIKTO [NIKTO ...]] [--dirble DIRBLE [DIRBLE ...]]
            [--testssl TESTSSL [TESTSSL ...]]
            [--fortify FORTIFY [FORTIFY ...]] [--nmap-state NMAP_STATE]
            [--nmap-services] [--no-nessus-autoclassify]
            [--nessus-autoclassify-file NESSUS_AUTOCLASSIFY_FILE]
            [--nessus-tls-file NESSUS_TLS_FILE]
            [--nessus-x509-file NESSUS_X509_FILE]
            [--nessus-http-file NESSUS_HTTP_FILE]
            [--nessus-smb-file NESSUS_SMB_FILE]
            [--nessus-rdp-file NESSUS_RDP_FILE]
            [--nessus-ssh-file NESSUS_SSH_FILE]
            [--nessus-min-severity NESSUS_MIN_SEVERITY]
            [--nessus-plugin-name-width NESSUS_PLUGIN_NAME_WIDTH]
            [--nessus-sort-by NESSUS_SORT_BY]
            [--nikto-description-width NIKTO_DESCRIPTION_WIDTH]
            [--fortify-details] [--annotation-width ANNOTATION_WIDTH]
            [-oC OUTPUT_CSV] [-oT OUTPUT_TXT] [-oX OUTPUT_XLSX]
            [-oA OUTPUT_ALL]

Converting scanning reports to a tabular format

optional arguments:
  -h, --help            show this help message and exit
  --nmap-state NMAP_STATE
                        Specify the desired state to filter (e.g.
                        open|filtered).
  --nmap-services       Specify to ouput a supplemental list of detected
                        services.
  --no-nessus-autoclassify
                        Specify to not autoclassify Nessus results.
  --nessus-autoclassify-file NESSUS_AUTOCLASSIFY_FILE
                        Specify to override a custom Nessus autoclassify YAML
                        file.
  --nessus-tls-file NESSUS_TLS_FILE
                        Specify to override a custom Nessus TLS findings YAML
                        file.
  --nessus-x509-file NESSUS_X509_FILE
                        Specify to override a custom Nessus X.509 findings
                        YAML file.
  --nessus-http-file NESSUS_HTTP_FILE
                        Specify to override a custom Nessus HTTP findings YAML
                        file.
  --nessus-smb-file NESSUS_SMB_FILE
                        Specify to override a custom Nessus SMB findings YAML
                        file.
  --nessus-rdp-file NESSUS_RDP_FILE
                        Specify to override a custom Nessus RDP findings YAML
                        file.
  --nessus-ssh-file NESSUS_SSH_FILE
                        Specify to override a custom Nessus SSH findings YAML
                        file.
  --nessus-min-severity NESSUS_MIN_SEVERITY
                        Specify the minimum severity to output (e.g. 1).
  --nessus-plugin-name-width NESSUS_PLUGIN_NAME_WIDTH
                        Specify the width of the pluginid column (e.g. 30).
  --nessus-sort-by NESSUS_SORT_BY
                        Specify to sort output by ip-address, port, plugin-id,
                        plugin-name or severity.
  --nikto-description-width NIKTO_DESCRIPTION_WIDTH
                        Specify the width of the description column (e.g. 30).
  --fortify-details     Specify to include the Fortify abstracts, explanations
                        and recommendations for each vulnerability.
  --annotation-width ANNOTATION_WIDTH
                        Specify the width of the annotation column (e.g. 30).
  -oC OUTPUT_CSV, --output-csv OUTPUT_CSV
                        Specify the output CSV basename (e.g. output).
  -oT OUTPUT_TXT, --output-txt OUTPUT_TXT
                        Specify the output TXT file (e.g. output.txt).
  -oX OUTPUT_XLSX, --output-xlsx OUTPUT_XLSX
                        Specify the output XLSX file (e.g. output.xlsx). Only
                        for Nessus at the moment
  -oA OUTPUT_ALL, --output-all OUTPUT_ALL
                        Specify the output basename to output to all formats
                        (e.g. output).

specify at least one:
  --nessus NESSUS [NESSUS ...]
                        Specify (multiple) Nessus XML files.
  --nmap NMAP [NMAP ...]
                        Specify (multiple) Nmap XML files.
  --nikto NIKTO [NIKTO ...]
                        Specify (multiple) Nikto XML files.
  --dirble DIRBLE [DIRBLE ...]
                        Specify (multiple) Dirble XML files.
  --testssl TESTSSL [TESTSSL ...]
                        Specify (multiple) Testssl JSON files.
  --fortify FORTIFY [FORTIFY ...]
                        Specify (multiple) HP Fortify FPR files.
```

## Example

A few examples

### Nessus

To produce an XLSX format:

```
$ sr2t --nessus example/nessus.nessus --no-nessus-autoclassify -oX example.xlsx
```

![Nessus XLSX Critical](example/nessus-xlsx-critical.png)

![Nessus XLSX Portscan](example/nessus-xlsx-portscan.png)

![Nessus XLSX TLS](example/nessus-xlsx-tls.png)

![Nessus XLSX X.509](example/nessus-xlsx-x509.png)

To produce an text tabular format to stdout:

```
$ sr2t --nessus example/nessus.nessus
+---------------+-------+-----------+-----------------------------------------------------------------------------+----------+-------------+
|       host    |  port | plugin id |                                 plugin name                                 | severity | annotations |
+---------------+-------+-----------+-----------------------------------------------------------------------------+----------+-------------+
| 192.168.142.4 | 3389  |   42873   | SSL Medium Strength Cipher Suites Supported (SWEET32)                       |    2     |      X      |
| 192.168.142.4 | 443   |   42873   | SSL Medium Strength Cipher Suites Supported (SWEET32)                       |    2     |      X      |
| 192.168.142.4 | 3389  |   18405   | Microsoft Windows Remote Desktop Protocol Server Man-in-the-Middle Weakness |    2     |      X      |
| 192.168.142.4 | 3389  |   30218   | Terminal Services Encryption Level is not FIPS-140 Compliant                |    1     |      X      |
| 192.168.142.4 | 3389  |   57690   | Terminal Services Encryption Level is Medium or Low                         |    2     |      X      |
| 192.168.142.4 | 3389  |   58453   | Terminal Services Doesn't Use Network Level Authentication (NLA) Only       |    2     |      X      |
| 192.168.142.4 | 3389  |   45411   | SSL Certificate with Wrong Hostname                                         |    2     |      X      |
| 192.168.142.4 | 443   |   45411   | SSL Certificate with Wrong Hostname                                         |    2     |      X      |
| 192.168.142.4 | 3389  |   35291   | SSL Certificate Signed Using Weak Hashing Algorithm                         |    2     |      X      |
| 192.168.142.4 | 3389  |   57582   | SSL Self-Signed Certificate                                                 |    2     |      X      |
| 192.168.142.4 | 3389  |   51192   | SSL Certificate Cannot Be Trusted                                           |    2     |      X      |
| 192.168.142.2 | 3389  |   42873   | SSL Medium Strength Cipher Suites Supported (SWEET32)                       |    2     |      X      |
| 192.168.142.2 | 443   |   42873   | SSL Medium Strength Cipher Suites Supported (SWEET32)                       |    2     |      X      |
| 192.168.142.2 | 3389  |   18405   | Microsoft Windows Remote Desktop Protocol Server Man-in-the-Middle Weakness |    2     |      X      |
| 192.168.142.2 | 3389  |   30218   | Terminal Services Encryption Level is not FIPS-140 Compliant                |    1     |      X      |
| 192.168.142.2 | 3389  |   57690   | Terminal Services Encryption Level is Medium or Low                         |    2     |      X      |
| 192.168.142.2 | 3389  |   58453   | Terminal Services Doesn't Use Network Level Authentication (NLA) Only       |    2     |      X      |
| 192.168.142.2 | 3389  |   45411   | SSL Certificate with Wrong Hostname                                         |    2     |      X      |
| 192.168.142.2 | 443   |   45411   | SSL Certificate with Wrong Hostname                                         |    2     |      X      |
| 192.168.142.2 | 3389  |   35291   | SSL Certificate Signed Using Weak Hashing Algorithm                         |    2     |      X      |
| 192.168.142.2 | 3389  |   57582   | SSL Self-Signed Certificate                                                 |    2     |      X      |
| 192.168.142.2 | 3389  |   51192   | SSL Certificate Cannot Be Trusted                                           |    2     |      X      |
| 192.168.142.2 | 445   |   57608   | SMB Signing not required                                                    |    2     |      X      |
+---------------+-------+-----------+-----------------------------------------------------------------------------+----------+-------------+
```

Or to output a CSV file:

```
$ sr2t --nessus example/nessus.nessus -oC example
$ cat example_nessus.csv
host,port,plugin id,plugin name,severity,annotations
192.168.142.4,3389,42873,SSL Medium Strength Cipher Suites Supported (SWEET32),2,X
192.168.142.4,443,42873,SSL Medium Strength Cipher Suites Supported (SWEET32),2,X
192.168.142.4,3389,18405,Microsoft Windows Remote Desktop Protocol Server Man-in-the-Middle Weakness,2,X
192.168.142.4,3389,30218,Terminal Services Encryption Level is not FIPS-140 Compliant,1,X
192.168.142.4,3389,57690,Terminal Services Encryption Level is Medium or Low,2,X
192.168.142.4,3389,58453,Terminal Services Doesn't Use Network Level Authentication (NLA) Only,2,X
192.168.142.4,3389,45411,SSL Certificate with Wrong Hostname,2,X
192.168.142.4,443,45411,SSL Certificate with Wrong Hostname,2,X
192.168.142.4,3389,35291,SSL Certificate Signed Using Weak Hashing Algorithm,2,X
192.168.142.4,3389,57582,SSL Self-Signed Certificate,2,X
192.168.142.4,3389,51192,SSL Certificate Cannot Be Trusted,2,X
192.168.142.2,3389,42873,SSL Medium Strength Cipher Suites Supported (SWEET32),2,X
192.168.142.2,443,42873,SSL Medium Strength Cipher Suites Supported (SWEET32),2,X
192.168.142.2,3389,18405,Microsoft Windows Remote Desktop Protocol Server Man-in-the-Middle Weakness,2,X
192.168.142.2,3389,30218,Terminal Services Encryption Level is not FIPS-140 Compliant,1,X
192.168.142.2,3389,57690,Terminal Services Encryption Level is Medium or Low,2,X
192.168.142.2,3389,58453,Terminal Services Doesn't Use Network Level Authentication (NLA) Only,2,X
192.168.142.2,3389,45411,SSL Certificate with Wrong Hostname,2,X
192.168.142.2,443,45411,SSL Certificate with Wrong Hostname,2,X
192.168.142.2,3389,35291,SSL Certificate Signed Using Weak Hashing Algorithm,2,X
192.168.142.2,3389,57582,SSL Self-Signed Certificate,2,X
192.168.142.2,3389,51192,SSL Certificate Cannot Be Trusted,2,X
192.168.142.2,445,57608,SMB Signing not required,2,X
```

### Nmap

To produce an XLSX format:

```
$ sr2t --nmap example/nmap.xml -oX example.xlsx
```

![Nmap XLSX](example/nmap-xlsx.png)

To produce an text tabular format to stdout:

```
$ sr2t --nmap example/nmap.xml --nmap-services
Nmap TCP:
+-----------------+----+----+----+-----+-----+-----+-----+------+------+------+
|                 | 53 | 80 | 88 | 135 | 139 | 389 | 445 | 3389 | 5800 | 5900 |
+-----------------+----+----+----+-----+-----+-----+-----+------+------+------+
| 192.168.23.78   | X  |    | X  |  X  |  X  |  X  |  X  |  X   |      |      |
| 192.168.27.243  |    |    |    |  X  |  X  |     |  X  |  X   |  X   |  X   |
| 192.168.99.164  |    |    |    |  X  |  X  |     |  X  |  X   |  X   |  X   |
| 192.168.228.211 |    | X  |    |     |     |     |     |      |      |      |
| 192.168.171.74  |    |    |    |  X  |  X  |     |  X  |  X   |  X   |  X   |
+-----------------+----+----+----+-----+-----+-----+-----+------+------+------+

Nmap Services:
+-----------------+------+-------+---------------+-------+
| ip address      | port | proto | service       | state |
+-----------------+------+-------+---------------+-------+
| 192.168.23.78   | 53   | tcp   | domain        | open  |
| 192.168.23.78   | 88   | tcp   | kerberos-sec  | open  |
| 192.168.23.78   | 135  | tcp   | msrpc         | open  |
| 192.168.23.78   | 139  | tcp   | netbios-ssn   | open  |
| 192.168.23.78   | 389  | tcp   | ldap          | open  |
| 192.168.23.78   | 445  | tcp   | microsoft-ds  | open  |
| 192.168.23.78   | 3389 | tcp   | ms-wbt-server | open  |
| 192.168.27.243  | 135  | tcp   | msrpc         | open  |
| 192.168.27.243  | 139  | tcp   | netbios-ssn   | open  |
| 192.168.27.243  | 445  | tcp   | microsoft-ds  | open  |
| 192.168.27.243  | 3389 | tcp   | ms-wbt-server | open  |
| 192.168.27.243  | 5800 | tcp   | vnc-http      | open  |
| 192.168.27.243  | 5900 | tcp   | vnc           | open  |
| 192.168.99.164  | 135  | tcp   | msrpc         | open  |
| 192.168.99.164  | 139  | tcp   | netbios-ssn   | open  |
| 192.168.99.164  | 445  | tcp   | microsoft-ds  | open  |
| 192.168.99.164  | 3389 | tcp   | ms-wbt-server | open  |
| 192.168.99.164  | 5800 | tcp   | vnc-http      | open  |
| 192.168.99.164  | 5900 | tcp   | vnc           | open  |
| 192.168.228.211 | 80   | tcp   | http          | open  |
| 192.168.171.74  | 135  | tcp   | msrpc         | open  |
| 192.168.171.74  | 139  | tcp   | netbios-ssn   | open  |
| 192.168.171.74  | 445  | tcp   | microsoft-ds  | open  |
| 192.168.171.74  | 3389 | tcp   | ms-wbt-server | open  |
| 192.168.171.74  | 5800 | tcp   | vnc-http      | open  |
| 192.168.171.74  | 5900 | tcp   | vnc           | open  |
+-----------------+------+-------+---------------+-------+
```

Or to output a CSV file:

```
$ sr2t --nmap example/nmap.xml -oC example
$ cat example_nmap_tcp.csv
ip address,53,80,88,135,139,389,445,3389,5800,5900
192.168.23.78,X,,X,X,X,X,X,X,,
192.168.27.243,,,,X,X,,X,X,X,X
192.168.99.164,,,,X,X,,X,X,X,X
192.168.228.211,,X,,,,,,,,
192.168.171.74,,,,X,X,,X,X,X,X
```

### Nikto

To produce an XLSX format:

```
$ sr2t --nikto example/nikto.xml -oX example/nikto.xlsx
```

![Nikto XLSX](example/nikto-xlsx.png)

To produce an text tabular format to stdout:

```
$ sr2t --nikto example/nikto.xml
+----------------+-----------------+-------------+----------------------------------------------------------------------------------+-------------+
| target ip      | target hostname | target port | description                                                                      | annotations |
+----------------+-----------------+-------------+----------------------------------------------------------------------------------+-------------+
| 192.168.178.10 | 192.168.178.10  | 80          | The anti-clickjacking X-Frame-Options header is not present.                     |      X      |
| 192.168.178.10 | 192.168.178.10  | 80          | The X-XSS-Protection header is not defined. This header can hint to the user     |      X      |
|                |                 |             | agent to protect against some forms of XSS                                       |             |
| 192.168.178.10 | 192.168.178.10  | 80          | The X-Content-Type-Options header is not set. This could allow the user agent to |      X      |
|                |                 |             | render the content of the site in a different fashion to the MIME type           |             |
+----------------+-----------------+-------------+----------------------------------------------------------------------------------+-------------+
```

Or to output a CSV file:

```
$ sr2t --nikto example/nikto.xml -oC example
$ cat example_nikto.csv
target ip,target hostname,target port,description,annotations
192.168.178.10,192.168.178.10,80,The anti-clickjacking X-Frame-Options header is not present.,X
192.168.178.10,192.168.178.10,80,"The X-XSS-Protection header is not defined. This header can hint to the user
agent to protect against some forms of XSS",X
192.168.178.10,192.168.178.10,80,"The X-Content-Type-Options header is not set. This could allow the user agent to
render the content of the site in a different fashion to the MIME type",X
```

### Dirble

To produce an XLSX format:

```
$ sr2t --dirble example/dirble.xml -oX example.xlsx
```

![Dirble XLSX](example/dirble-xlsx.png)

To produce an text tabular format to stdout:

```
$ sr2t --dirble example/dirble.xml
+-----------------------------------+------+-------------+--------------+-------------+---------------------+--------------+-------------+
| url                               | code | content len | is directory | is listable | found from listable | redirect url | annotations |
+-----------------------------------+------+-------------+--------------+-------------+---------------------+--------------+-------------+
| http://example.org/flv            | 0    | 0           | false        | false       | false               |              |      X      |
| http://example.org/hire           | 0    | 0           | false        | false       | false               |              |      X      |
| http://example.org/phpSQLiteAdmin | 0    | 0           | false        | false       | false               |              |      X      |
| http://example.org/print_order    | 0    | 0           | false        | false       | false               |              |      X      |
| http://example.org/putty          | 0    | 0           | false        | false       | false               |              |      X      |
| http://example.org/receipts       | 0    | 0           | false        | false       | false               |              |      X      |
+-----------------------------------+------+-------------+--------------+-------------+---------------------+--------------+-------------+
```

Or to output a CSV file:

```
$ sr2t --dirble example/dirble.xml -oC example
$ cat example_dirble.csv
url,code,content len,is directory,is listable,found from listable,redirect url,annotations
http://example.org/flv,0,0,false,false,false,,X
http://example.org/hire,0,0,false,false,false,,X
http://example.org/phpSQLiteAdmin,0,0,false,false,false,,X
http://example.org/print_order,0,0,false,false,false,,X
http://example.org/putty,0,0,false,false,false,,X
http://example.org/receipts,0,0,false,false,false,,X

```

### Testssl

To produce an XLSX format:

```
$ sr2t --testssl example/testssl.json -oX example.xlsx
```

![Testssl XLSX](example/testssl-xlsx.png)

To produce an text tabular format to stdout:

```
$ sr2t --testssl example/testssl.json
+-----------------------------------+------+--------+---------+--------+------------+-----+---------+---------+----------+
| ip address                        | port | BREACH | No HSTS | No PFS | No TLSv1.3 | RC4 | TLSv1.0 | TLSv1.1 | Wildcard |
+-----------------------------------+------+--------+---------+--------+------------+-----+---------+---------+----------+
| rc4-md5.badssl.com/104.154.89.105 | 443  |   X    |    X    |   X    |     X      |  X  |    X    |    X    |    X     |
+-----------------------------------+------+--------+---------+--------+------------+-----+---------+---------+----------+
```

Or to output a CSV file:

```
$ sr2t --testssl example/testssl.json -oC example
$ cat example_testssl.csv
ip address,port,BREACH,No HSTS,No PFS,No TLSv1.3,RC4,TLSv1.0,TLSv1.1,Wildcard
rc4-md5.badssl.com/104.154.89.105,443,X,X,X,X,X,X,X,X
```

### Fortify

To produce an XLSX format:

```
$ sr2t --fortify example/fortify.fpr -oX example.xlsx
```

![Fortify XLSX](example/fortify-xlsx.png)

To produce an text tabular format to stdout:

```
$ sr2t --fortify example/fortify.fpr
+--------------------------+-----------------------+-------------------------------+----------+------------+-------------+
|                          |          type         |            subtype            | severity | confidence | annotations |
+--------------------------+-----------------------+-------------------------------+----------+------------+-------------+
| example1/web.xml:135:135 | J2EE Misconfiguration | Insecure Transport            |   3.0    |    5.0     |      X      |
| example2/web.xml:150:150 | J2EE Misconfiguration | Insecure Transport            |   3.0    |    5.0     |      X      |
| example3/web.xml:109:109 | J2EE Misconfiguration | Incomplete Error Handling     |   3.0    |    5.0     |      X      |
| example4/web.xml:108:108 | J2EE Misconfiguration | Incomplete Error Handling     |   3.0    |    5.0     |      X      |
| example5/web.xml:166:166 | J2EE Misconfiguration | Insecure Transport            |   3.0    |    5.0     |      X      |
| example6/web.xml:2:2     | J2EE Misconfiguration | Excessive Session Timeout     |   3.0    |    5.0     |      X      |
| example7/web.xml:162:162 | J2EE Misconfiguration | Missing Authentication Method |   3.0    |    5.0     |      X      |
+--------------------------+-----------------------+-------------------------------+----------+------------+-------------+
```

Or to output a CSV file:

```
$ sr2t --fortify example/fortify.fpr -oC example
$ cat example_fortify.csv
,type,subtype,severity,confidence,annotations
example1/web.xml:135:135,J2EE Misconfiguration,Insecure Transport,3.0,5.0,X
example2/web.xml:150:150,J2EE Misconfiguration,Insecure Transport,3.0,5.0,X
example3/web.xml:109:109,J2EE Misconfiguration,Incomplete Error Handling,3.0,5.0,X
example4/web.xml:108:108,J2EE Misconfiguration,Incomplete Error Handling,3.0,5.0,X
example5/web.xml:166:166,J2EE Misconfiguration,Insecure Transport,3.0,5.0,X
example6/web.xml:2:2,J2EE Misconfiguration,Excessive Session Timeout,3.0,5.0,X
example7/web.xml:162:162,J2EE Misconfiguration,Missing Authentication Method,3.0,5.0,X
```
