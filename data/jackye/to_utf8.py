import codecs
BLOCKSIZE = 1048576 # or some other, desired size in bytes
with codecs.open("invasive_all.csv", "r", "iso-8859-1") as sourceFile:
    with codecs.open("invasive_utf8.csv", "w", "utf-8") as targetFile:
        while True:
            contents = sourceFile.read(BLOCKSIZE)
            if not contents:
                break
            targetFile.write(contents)