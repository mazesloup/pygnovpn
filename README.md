# pygnovpn

Helper to convert .ovpn file to network-manager-gnome readable format

It's generate 4 or 5 files from one .ovpn file
 - .ovpn without cert and key
 - CA cert
 - Client cert
 - Client Key
 - TA key
 
It disable some option (reneg-sec by default know for crash at import), more option can be disable by pass them at command line

## Getting Started


### Prerequisites

Python > 2

### Usage
```
usage: pygnovpn.py [-h] [-c] [-q] [-d DISABLE] infile outdir

Helper to convert .ovpn to network-manager-gnome readable format

positional arguments:
  infile                .ovpn input file
  outdir                destination directory for output files

optional arguments:
  -h, --help            show this help message and exit
  -c, --create-dir      If specified, output dir will be created if not exists
  -q, --quiet           No output, not quering for create folder, use
                        --create-dir to auto-create
  -d DISABLE, --disable-options DISABLE
                        Append options to disable while exporting
                        configuration, can have more than one

```

## Author

* **Mathieu Courquin** [mathieu@mat-ik.fr](mailto:mathieu@mat-ik.fr) - *Initial work* - [MazeSloup](https://mat-ik.fr)


## License

This project is licensed under the  GNU General Public License v3.0 - see the [LICENSE.md](LICENSE.md) file for details
