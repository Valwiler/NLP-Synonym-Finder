import sys
import time
import trainer as t
import reader as r
import processor as p
import chrono as ch

def main(window, encoding, paths):
    # paths = []
    # window = int(sys.argv[1])
    # encoding = str(sys.argv[2])
    # for path in sys.argv[3:]:
    #     paths.append(path)
    chrono = ch.Chrono()
    chrono.start()
    reader = r.Reader(encoding, paths)
    reader.read()
    chrono.end()
    chrono.log('reader ok : ')
    chrono.start()
    text_processor = p.Processor(window, reader.full_text)
    text_processor.process_text()
    chrono.end()
    chrono.log('text processing ok : ')
    chrono.start()
    #trainer = t.Trainer("bras", text_processor.result_array, text_processor.index_to_word, text_processor.word_to_index)
    #trainer.training()
    chrono.end()
    chrono.log('training ok : ')


if __name__ == '__main__':
    main(5, 'utf-8', ['LesTroisMousquetairesUTF8.txt', 'LeVentreDeParisUTF8.txt', 'GerminalUTF8.txt'])
    #main(4, 'utf-8', ['coucou.txt'])
