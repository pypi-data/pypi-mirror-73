
import subprocess, os

abspath = os.path.abspath(__file__)[:-10]
#print("abspath: ", abspath)

def pos_tagging(sentence):
    # korea univ morpheme analyzer
    m_command = "cd " + abspath + "data/kmat/bin/;./kmat <<<\'" + sentence + "\' 2>/dev/null"
    result = subprocess.check_output(m_command.encode(encoding='cp949', errors='ignore'), shell=True, executable='/bin/bash')

    mor_name_lists = []
    mor_tags_lists = []

    for each in result.decode(encoding='cp949', errors='ignore').split('\n'):
        if len(each) > 0:
            try:
                mor_texts = each.split('\t')[1]
            except:
                print(each)
            mor_results = mor_texts.split('+')

            for each_mor in mor_results:
                try:
                    mor_name_lists.append(each_mor.split('/')[0])
                    mor_tags_lists.append(each_mor.split('/')[1])
                except:
                    mor_name_lists.append(each_mor.split('/')[0])
                    mor_tags_lists.append(each_mor.split('/')[1])


    mor_analyzed = [(x,mor_tags_lists[i]) for i, x in enumerate(mor_name_lists)]


    return mor_analyzed


def morphs(sentence):
    # korea univ morpheme analyzer
    sentence.encode('utf-8').decode('utf-8')
    m_command = "cd " + abspath + "data/kmat/bin/;./kmat <<<\'" + sentence + "\' 2>/dev/null"
    result = subprocess.check_output(m_command.encode(encoding='cp949', errors='ignore'), shell=True,
                                     executable='/bin/bash')
    mor_name_lists = []

    for each in result.decode(encoding='cp949', errors='ignore').split('\n'):
        if len(each) > 0:
            try:
                mor_texts = each.split('\t')[1]
            except:
                print(each)
            mor_results = mor_texts.split('+')

            for each_mor in mor_results:
                try:
                    mor_name_lists.append(each_mor.split('/')[0])
                except:
                    mor_name_lists.append(each_mor.split('/')[0])


    return mor_name_lists


def pos(sentence):

    # korea univ morpheme analyzer
    sentence.encode('utf-8').decode('utf-8')
    m_command = "cd " + abspath + "data/kmat/bin/;./kmat <<<\'" + sentence + "\' 2>/dev/null"
    #print("mcommand: ", m_command)
    result = subprocess.check_output(m_command.encode(encoding='cp949', errors='ignore'), shell=True,
                                     executable='/bin/bash')
    mor_tags_lists = []

    for each in result.decode(encoding='cp949', errors='ignore').split('\n'):
        if len(each) > 0:
            try:
                mor_texts = each.split('\t')[1]
            except:
                print(each)
            mor_results = mor_texts.split('+')

            for each_mor in mor_results:
                try:
                    mor_tags_lists.append(each_mor.split('/')[1])
                except:
                    mor_tags_lists.append('SS')

    return mor_tags_lists

def nouns(sentence):
    # korea univ morpheme analyzer
    sentence.encode('utf-8').decode('utf-8')
    m_command = "cd " + abspath + "data/kmat/bin/;./kmat <<<\'" + sentence + "\' 2>/dev/null"
    #print("mcommand: ", m_command)
    result = subprocess.check_output(m_command.encode(encoding='cp949', errors='ignore'), shell=True,
                                     executable='/bin/bash')
    mor_name_lists = []
    mor_tags_lists = []

    for each in result.decode(encoding='cp949', errors='ignore').split('\n'):
        if len(each) > 0:
            try:
                mor_texts = each.split('\t')[1]
            except:
                print(each)
            mor_results = mor_texts.split('+')

            for each_mor in mor_results:
                try:
                    mor_name_lists.append(each_mor.split('/')[0])
                    mor_tags_lists.append(each_mor.split('/')[1])
                except:
                    mor_name_lists.append(each_mor.split('/')[0])
                    mor_tags_lists.append(each_mor.split('/')[1])


    noun_lists = [mor_name_lists[i] for i, x in enumerate(mor_tags_lists) if x.startswith('N') == True]

    return noun_lists


if __name__ == "__main__":
    sentence = "안녕하세요."
    #print("input: ", sentence)
    print("pos_tagging: ", pos_tagging(sentence))
    #print("morphs: ", morphs(sentence))
    #print("pos: ", pos(sentence))
    #print("nouns: ", nouns(sentence))