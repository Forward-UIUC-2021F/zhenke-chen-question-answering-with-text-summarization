# Run with 'qagoogle' conda environment on osprey2

import re
import json

from retrieval import select_paragraphs 
from collect_data import fetch_candidate_texts

from tqdm import tqdm
import threading
import sys

import time


data_root_dir = "data/articles"
outlines_file = "data/generated_outlines_csdefs_full.txt"

word_re = re.compile("\s\w{3}\w*", re.IGNORECASE)

def filter_text(text, min_words=20):
    # Check first character is capital
    is_par_start = text[0].isupper()
    if not is_par_start:
        return False

    # Check min number of words
    num_words = len(re.findall(word_re, text))
    if num_words < min_words:
        return False 

    return True


def get_top_passages(question, num_paragraphs = 3, verbose=False):
    url_passages = fetch_candidate_texts(question, num_websites=15, text_filter=filter_text)

    if verbose:
        print("Found website data: ")
        print(json.dumps(url_passages, indent=4))

    # Aggregate all passages in one variable
    passages = []
    for u_i in range(len(url_passages)):
        u_data = url_passages[u_i]
        u_passages = u_data["passages"]

        for p_i in range(len(u_passages)):
            p = u_passages[p_i]
            # p_meta = (u_i, p_i)
            p_meta = {
                'url': u_data["url"]
            }

            passages.append([p_meta, p])

    # Rank the top  passages from candidates
    ranked_passages = select_paragraphs(question, passages, num_paragraphs)

    if verbose:
        print("Final ranked output:")
        print(json.dumps(ranked_passages, indent=4))

    return ranked_passages


def generate_article(keyword, sections, verbose=True):

    if verbose:
        print("Generating article for keyword:", keyword)

    section_to_content = {}

    for s in sections:

        # Query to google search
        query = s 
        if keyword.lower() not in s.lower():
            query = keyword + " " + s


        passages = get_top_passages(query)

        section_to_content[s] = passages

        if verbose:
            print("\t(*) Section", s, ':')

            for p in passages:
                print("\t", p)

    return section_to_content
    

def save_article(keyword, sections, verbose=True):
    sections_content = generate_article(keyword, sections, verbose=verbose)
    res_obj = {
        'keyword': keyword, 
        'article': sections_content
    }

    with open(f"{data_root_dir}/{keyword}.json", "w") as f:
        json.dump(res_obj, f, indent=4)

    time.sleep(10)


def parse_outlines(filename):
    outlines = []
    with open(filename) as f:
        f_lines = f.read().split('\n')

    for i in range(0, len(f_lines), 6):
        if i + 6 >= len(f_lines):
            continue

        cur_elem_lines = f_lines[i:i+6]

        keyword = cur_elem_lines[0].split(' [EOT] ')[0]
        outline = cur_elem_lines[3].split(' [SEP] ')

        # print(keyword, outline)
        outlines.append({
            'keyword': keyword,
            'outline': outline
        })
    
    return outlines


def gen_articles_parallel(article_outlines, num_threads = 1):

    threads = []
    new_task_lock = threading.Lock()

    pbar = tqdm(total=len(article_outlines), file=sys.stdout)


    def worker():
        while True:
            # Get next article to generate
            new_task_lock.acquire()
            if len(article_outlines) == 0:
                new_task_lock.release()
                return
            
            cur_outline = article_outlines.pop()
            new_task_lock.release()

            # Generate and save article
            keyword = cur_outline['keyword']
            sections = cur_outline['outline']

            try:
                save_article(keyword, sections, verbose=False)
            except Exception as e:
                print(e)

            pbar.update(1)

    # Start thread pool
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=())
        t.start()

        threads.append(t)

    for t in threads:
        t.join()

    pbar.close()


if __name__ == '__main__':
    # start_idx = 0
    # num_articles = 512

    # article_outlines = parse_outlines(outlines_file)
    # article_outlines = article_outlines[start_idx : start_idx + num_articles]

    # article_kwds = [o['keyword'] for o in article_outlines]
    # print(article_kwds)
    # exit()
    
    # gen_articles_parallel(article_outlines)
    # exit()

    # save_article("Data structures", ["history", "types", "applications"])
    # save_article("machine learning", ["history", "applications"])
    # save_article("deep learning", ["history", "applications"])

    # save_article("feature selection", ["Variations", "Overview", "Implementation", "Examples", "History"])
    # save_article("artificial intelligence", ["history", "applications", "Types of artificial intelligence"])
    # save_article("virtual reality", ["Technology", "History", "Applications", "Types of virtual reality"])
    # save_article("image processing", ["Overview", "History", "Applications", "Types"])

    # For demo
    save_article("computer architecture", ["Overview", "History", "Types of computer architecture", "Applications"])
    save_article("natural language processing", ["History", "Applications"])
    save_article("reinforcement learning", ["Overview", "Applications"])
    save_article("case-based reasoning", ["Overview", "History"])

    


