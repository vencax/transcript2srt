#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.sax import make_parser, handler
from datetime import datetime, timedelta

class SubParser(handler.ContentHandler):
    _suportDT = datetime(1970, 1, 1)
    _fmt = '%H:%M:%S'
    _itemStr = '%(cntr)i%(NL)s%(begin)s --> %(end)s%(NL)s%(cntnt)s%(NL)s%(NL)s'

    def __init__(self, outFile, nl):
        self._outFile = open(outFile, 'w')
        self._cntr = 0
        self._cntnt = ''
        self._nl = nl

    def startElement(self, name, attrs):
        if name == 'text':
            self._start = timedelta(seconds=float(attrs['start']))
            self._dur = timedelta(seconds=float(attrs['dur']))
                        
    def characters(self, content):
        self._cntnt += content
        
    def endElement(self, name):
        if name == 'text':
            self._cntr += 1
            beg = self._suportDT + self._start
            end = self._suportDT + self._start + self._dur
            self._outFile.write(self._itemStr % {
                'NL': self._nl,
                'cntr': self._cntr,
                'begin': self._to_time(beg),
                'end': self._to_time(end),
                'cntnt': self._cntnt
            })
            self._cntnt = ''
        
    def _to_time(self, delta):
        return '%s,%03i' % (delta.strftime(self._fmt), delta.microsecond/1000)

def convert(inputfile, outputfile, nl='\n'):
    parser = make_parser()
    parser.setContentHandler(SubParser(outputfile, nl))
    parser.parse(inputfile)


def usage():
    print '''sub2srt [OPTIONS] infile outfile
    -h, --help: prints help
    -w, --winlinebreaks: prints windoze linebreaks
    '''

if __name__ == "__main__":
    import sys, getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], ':hw', ['help', 'winlinebreaks'])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err)
        usage()
        sys.exit(2)
    nl = '\n'
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-w', '--winlinebreaks'):
            nl = '\r\n'
        else:
            assert False, 'unhandled option'
    
    args.append(nl)
    convert(*args)
