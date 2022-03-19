import re
import json

from retrieval import select_paragraphs 
from collect_data import fetch_candidate_texts

data_root_dir = "data"

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
            passages.append([(u_i, p_i), p])

    # Rank the top  passages from candidates
    ranked_passages = select_paragraphs(question, passages, num_paragraphs)

    if verbose:
        print("Final ranked output:")
        print(json.dumps(ranked_passages, indent=4))

    return ranked_passages


def generate_article(keyword, sections, verbose=False):

    if verbose:
        print("Generating article for keyword:", keyword)

    section_to_content = {}

    for s in sections:
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

    with open(f"{data_root_dir}/{keyword}.json", "w") as f:
        json.dump(sections_content, f, indent=4)

if __name__ == '__main__':
    keyword = "Support vector machine"
    sections = ["history", "applications", "variants"]

    save_article(keyword, sections)

    keyword = "Data structures"
    sections = ["history", "types", "applications"]

    save_article(keyword, sections)


