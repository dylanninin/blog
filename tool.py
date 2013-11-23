#!/usr/bin/env python
"""ToolKit.

version 1.0
history:
2013-6-19    dylanninin@gmail.com    init
2013-11-23    dylanninin@gmail.com     update tags, categories

"""
# -*- coding: utf-8 -*-

import yaml


class Extract:
    """Extrace tool."""

    def __init__(self):
        """
        #TODO: FIXME: init
        """
        self.stop_words = []
        self.categories = ['Web', 'Linux', 'Database', 'Development']

    def auto_keyphrase(self, entry):
        """
        #TODO: FIXME: extract keyphrase automaticly

        reference:
            http://www.ruanyifeng.com/blog/2013/03/tf-idf.html
        """
        return self.categories

    def auto_categories(self, entry):
        """
        #TODO: FIXME: extract categories automaticly
        """
        return self.categories

    def auto_summarization(self, entry):
        """
        #TODO: FIXME: extract summarization automaticly

        reference:
            http://www.ruanyifeng.com/blog/2013/03/automatic_summarization.html
        """
        return entry.content[:200]

    def auto_similiarities(self, entry, entries):
        """
        #TODO: FIXME: extract similiarities  automaticly

        reference:
            http://www.ruanyifeng.com/blog/2013/03/cosine_similarity.html
        """
        return entries


    def parse(self, entry):
        """
        parse the raw content of a markdown entry
        TODO: FIXME

        args:
            filename:    the filename of a markdown entry

        return:
            a tuple like (yaml_header, title, categories, tags)
            the content will be preprocessed if it does have a yaml header declaration.

        yaml header field options:
            title
            category or categories
            tags

        blog example:
            ---
            title: the title, default None if it's empty
            category: category, default Uncategorised if it's empty.
            tags: [tag1, tag2], default [Untagged] if it's empty.
            ---

            ##header
            the content of the blog
            blah blah ...
            ... ...

        reference:
            http://jekyllrb.com/docs/frontmatter/

        """
        seperators = ['---\n', '---\r\n']
        newlines = ['\n', '\r\n']
        title = None
        categories = ['Uncategorised']
        tags = ['Untagged']
        number = 4
        yml = []
        header = ''
        with open(entry.path, 'r') as f:
            first = f.readline()
            if first in seperators:
                count, line = 1, f.readline()
                while count <= number and not line in seperators:
                    yml.append(line)
                    line = f.readline()
                    count += 1
                if len(yml) == 0 or not line in seperators or not f.readline() in newlines:
                    msg = 'Error, YAML header declaration with %s does not match in %s ' % (seperators, md)
                    print msg
                skip = count + 2
                f.seek(0)
                header = ''.join([f.readline() for i in xrange(skip)])
        yml = ''.join(yml)
        if not yml == '':
            y = yaml.load(yml)
            title = y.get('title') or title
            categories = y.get('categories') or categories
            category = y.get('category')
            if not category == None:
                categories = [category]
            tags = y.get('tags')
        return header, title, categories, tags


class Dict2Object(dict):
    """
    dict to object
    so you can access like a.attribute but not a['attribute']

    reference:
        http://stackoverflow.com/questions/1305532/convert-python-dict-to-object
    """
    def __init__(self, data = None):
        super(Dict2Object, self).__init__()
        if data:
            self.__update(data, {})

    def __update(self, data, did):
        dataid = id(data)
        did[dataid] = self

        for k in data:
            dkid = id(data[k])
            if did.has_key(dkid):
                self[k] = did[dkid]
            elif isinstance(data[k], Dict2Object):
                self[k] = data[k]
            elif isinstance(data[k], dict):
                obj = Dict2Object()
                obj.__update(data[k], did)
                self[k] = obj
                obj = None
            else:
                self[k] = data[k]

    def __getattr__(self, key):
        return self.get(key, None)

    def __setattr__(self, key, value):
        if isinstance(value,dict):
            self[key] = Dict2Object(value)
        else:
            self[key] = value

    def update(self, *args):
        for obj in args:
            for k in obj:
                if isinstance(obj[k],dict):
                    self[k] = Dict2Object(obj[k])
                else:
                    self[k] = obj[k]
        return self

    def merge(self, *args):
        for obj in args:
            for k in obj:
                if self.has_key(k):
                    if isinstance(self[k],list) and isinstance(obj[k],list):
                        self[k] += obj[k]
                    elif isinstance(self[k],list):
                        self[k].append(obj[k])
                    elif isinstance(obj[k],list):
                        self[k] = [self[k]] + obj[k]
                    elif isinstance(self[k],Dict2Object) and isinstance(obj[k],Dict2Object):
                        self[k].merge(obj[k] )
                    elif isinstance(self[k],Dict2Object) and isinstance(obj[k],dict):
                        self[k].merge(obj[k])
                    else:
                        self[k] = [self[k], obj[k]]
                else:
                    if isinstance(obj[k],dict):
                        self[k] = Dict2Object(obj[k])
                    else:
                        self[k] = obj[k]
        return self


if __name__ == '__main__':
    import doctest
    doctest.testmod()
