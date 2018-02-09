#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os


class pygnovpn:
    DEBUG = False
    infile = False
    outdir = False
    data = False
    filename = False
    ovpn = False
    ca = False
    cert = False
    key = False
    tls = False
    todisable = ['reneg-sec']

    def __init__(self, infile, outdir):
        self.infile = infile
        self.outdir = outdir
        self.filename = os.path.basename(self.infile)
        self.todisable = ['reneg-sec']
        self.printinfo('Analysing '+ self.infile)
        self.setdata()
        self.parsedata()


    def setdata(self):
        try:
            f = open(self.infile, "r")
            self.data = f.read()
            f.close()
        except Exception:
            self.printinfo('[!] Can\'t open '+self.infile)
            sys.exit(0)

    def parsedata(self):
        self.ovpn = self.data[0:self.data.find('<ca>')]
        self.cleandata()
        if self.data.find('<ca>') > -1:
            self.printinfo("Found CA")
            self.ca = self.data[self.data.find('<ca>')+4:self.data.find('</ca>')]
            self.savefile(self.ca, self.filename+"_ca.crt")
            self.ovpn = self.ovpn + "ca '" + os.path.join(self.outdir, self.filename + "_ca.crt'")
        if self.data.find('<cert>') > -1:
            self.printinfo("Found CERT")
            self.cert = self.data[self.data.find('<cert>')+6:self.data.find('</cert>')]
            self.savefile(self.cert, self.filename+"_cert.crt")
            self.ovpn = self.ovpn + "\ncert '" + os.path.join(self.outdir, self.filename + "_cert.crt'")
        if self.data.find('<key') > -1:
            self.printinfo("Found KEY")
            self.key = self.data[self.data.find('<key>')+5:self.data.find('</key>')]
            self.savefile(self.key, self.filename+"_key.key")
            self.ovpn = self.ovpn + "\nkey '" + os.path.join(self.outdir, self.filename + "_key.key'")
        if self.data.find('<tls-auth>') > -1:
            self.printinfo("Found TLS-AUTH")
            self.tls = self.data[self.data.find('<tls-auth>')+10:self.data.find('</tls-auth>')]
            self.savefile(self.tls, self.filename+"_ta.key")
            self.ovpn = self.ovpn + "\ntls-auth '" + os.path.join(self.outdir, self.filename + "_ta.key'")
        if self.DEBUG:
            self.printvalues()
        self.savefile(self.ovpn, self.filename+".ovpn")
        self.printinfo("Done. Files are saved in " + self.outdir)

    def cleandata(self):
        for r in self.todisable:
            self.ovpn = self.ovpn.replace(r, '#'+r)

    def savefile(self, data, filename):
        if data:
            try:
                fname = os.path.join(self.outdir, filename)
                f = open(fname, "w")
                data = os.linesep.join([s for s in data.splitlines() if s])
                f.write(data)
                f.close()
            except:
                self.printinfo("Can\'t save file " + fname + " exiting...")
                sys.exit(0)

    def printvalues(self):
        self.printinfo(self.ovpn)
        self.printinfo(self.ca)
        self.printinfo(self.cert)
        self.printinfo(self.key)

    def printinfo(self, s):
        print '->', s


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Helper to convert .ovpn to network-manager-gnome readable format')
    parser.add_argument('--ovpn', help='.ovpn input file', action='store', default=False, dest='infile')
    parser.add_argument('--dest', help='destination directory for output files', action='store',
                        default=False, dest='outdir')
    args = parser.parse_args()
    if (not args.infile) and (not args.outdir):
        parser.error('Please, specify two arguments')
        sys.exit(0)
    #do the stuff
    g = pygnovpn(args.infile, args.outdir)
