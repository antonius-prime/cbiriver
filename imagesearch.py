import pickle
from pysqlite2 import dbapi2 as sqlite
import numpy as np

class Indexer(object):
    """ This class is used for database indexing."""

    def __init__(self, db, voc):
        """Init"""
        self.con = sqlite.connect(db)
        self.voc = voc

    def __del__(self):
        """Close connection"""
        self.con.close()

    def db_commit(self):
        """Commit transaction"""
        self.con.commit()

    def create_tables(self):
        """Create the database tables."""

        self.con.execute('create table imlist(filename)')
        self.con.execute('create table imwords(imid,wordid,vocname)')
        self.con.execute('create table imhistograms(imid,histogram,vocname)')
        self.con.execute('create index im_idx on imlist(filename)')
        self.con.execute('create index wordid_idx on imwords(wordid)')
        self.con.execute('create index imid_idx on imwords(imid)')
        self.con.execute('create index imidhist_idx on imhistograms(imid)')
        self.db_commit()

    def add_to_index(self, imname, descr):
        """Take an image with feature descriptors,
        project on vocabulary and add to database.
        """
        if self.is_indexed(imname):
            return
        print 'indexing', imname

        # get the imid
        imid = self.get_id(imname)

        # get the words
        imwords = self.voc.project(descr)
        nbr_words = imwords.shape[0]

        # link each word to image
        for i in range(nbr_words):
            word = imwords[i]
            # wordid is the words number itself
            self.con.execute(\
                r"insert into imwords(imid, wordid, vocname) values (?,?,?)" \
                , (imid, word, self.voc.name))

        # store word histogram for image
        self.con.execute(\
        r"insert into imhistograms(imid,histogram,vocname) values(?,?,?)" \
        , (imid, pickle.dumps(imwords), self.voc.name))

    def is_indexed(self, imname):
        """ Returns True if imname has been indexed. """

        return self.con.execute(\
        "select rowid from imlist where filename='%s'" % imname).fetchone() \
        != None


    def get_id(self, imname):
        """ Get an entry id and add if not present. """

        cur = self.con.execute(\
        "select rowid from imlist where filename='%s'" % imname)

        res = cur.fetchone()
        if res == None:
            cur = self.con.execute(\
            "insert into imlist(filename) values ('%s')" % imname)
            return cur.lastrowid
        else:
            return res[0]


class Searcher(object):
    """ This class is used for database image searching."""

    def __init__(self, db, voc):
        """ Initialize with the database name and the vocabulary."""
        self.con = sqlite.connect(db)
        self.voc = voc

    def __def__(self):
        self.con.close()

    def candidates_from_word(self, imword):
        """ Extract list of images containing given word."""

        im_ids = self.con.execute(\
        "select distinct imid from imwords where wordid=%d" % imword).fetchall()

        return [i[0] for i in im_ids]

    def candidates_from_histogram(self, imwords):
        """ Get list of images with similar words. """

        # get the word ids
        words = imwords. nonzero()[0]

        # find candidates
        candidates = []
        for word in words:
            c = self.candidates_from_word(word)
            candidates += c

        # take all unique words and reverse sort on occurrence
        tmp = [(w, candidates.count(w)) for w in set(candidates)]
        tmp.sort(cmp=lambda x, y: cmp(x[1], y[1]))
        tmp.reverse()

        # return sorted list, best matches first
        return [w[0] for w in tmp]

    def get_imhistogram(self, imname):
        """ Return the word histogram og an image. """

        im_id = self.con.execute(\
        "select rowid from imlist where filename='%s'" % imname).fetchone()
        s = self.con.execute(\
        "select histogram from imhistograms where rowid='%d'" % im_id).fetchone()

        return pickle.loads(str(s[0]))

    def query(self, imname):
        """ Find a list of matching images for given image name. """

        h = self.get_imhistogram(imname)
        candidates = self.candidates_from_histogram(h)

        matchscores = []
        for imid in candidates:

            cand_name = self.con.execute("select filename from imlist where rowid='%d'" % imid).fetchone()
            cand_h = self.get_imhistogram(cand_name)
            cand_dist = np.sqrt(sum((h-cand_h)**2)) # L2 metric!!!!!!!!!!!!!!!1
            matchscores.append((cand_dist,imid))

        matchscores.sort()

        return matchscores

    def get_file_name(self, imid):
        """ Return the filename for an image id"""

        s = self.con.execute("select filename from imlist where rowid='%d'" % imid).fetchone()

        return s[0]


def compute_ukbench_score(src, imlist):
    """
    Returns the average number of correct images on the top some number
    results of queries.
    """

    nbr_results = 4
    nbr_images = len(imlist)
    pos = np.zeros((nbr_images, nbr_results))

    for i in range(nbr_images):
        pos[i] = [w[1]-1 for w in src.query(imlist[i])[:4]]

    score = np.array([(pos[i]//nbr_results) for i in range(nbr_images)])*1.0

    return np.sum(score) / (nbr_images)

def plot_results(src, res):
    """ Plot the results. """
    from matplotlib import pyplot as plt
    import Image

    plt.figure()
    nbr_results = len(res)
    for i in range(nbr_results):
        imname = src.get_file_name(res[i])
        plt.subplot(1, nbr_results, i+1)
        plt.imshow(np.array(Image.open(imname)))
        plt.axis('off')

    plt.show()
