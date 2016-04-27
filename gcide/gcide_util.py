import codecs
import StringIO
import os
import json
from copy import deepcopy

def index_gcide(gcide_dir):
    index = {}
    for fn in os.listdir(gcide_dir):
        fp = os.path.join(gcide_dir, fn)
        if not os.path.isfile(fp):
            continue
        with codecs.open(fp, 'r', 'utf-8') as ifp:
            for line in ifp:
                entry = json.loads(line)
                key = entry[u'key'].lower()
                if key not in index:
                    index[key] = []
                index[key].append(entry)
    return index

def normalize_entries(entries):
    new_entries = []
    for entry in entries:
        for sense in entry[u'senses']:
            new_entry = {}
            new_entry['word'] = entry[u'key'].lower()
            new_entry['source'] = 'gcide'
            if u'pos' not in entry:
                new_entry['pos'] = ''
            else:
                new_entry['pos'] = entry[u'pos'][0]
            new_entry['def'] = sense[u'def']
            new_entries.append(new_entry)
    return new_entries

def filter_entries(entries):
    ''' Remove entries with empty definition or POS '''
    new_entries = []
    for entry in entries:
        if u'pos' not in entry:
            continue
        if len(entry[u'pos'][0].strip()) == 0:
            continue
        if u'senses' not in entry:
            continue
        senses = []
        for sense in entry[u'senses']:
            if u'def' not in sense:
                continue
            if len(sense[u'def'].strip()) == 0:
                continue
            senses.append(sense)
        if len(senses) != len(entry[u'senses']):
            new_entry = deepcopy(entry)
            new_entry[u'senses'] = senses
        new_entries.append(entry)
    return new_entries
