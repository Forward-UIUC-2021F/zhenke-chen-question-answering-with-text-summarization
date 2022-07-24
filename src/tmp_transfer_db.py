import mysql.connector
import glob
import json

db = mysql.connector.connect(
  host="Osprey1.csl.illinois.edu",
  user="aukey2",
  password="[removed]",
  database="keyword_pages"
)
cur = db.cursor()


def get_kw_id(keyword):
    cur.execute("SELECT id FROM keyword WHERE name = %s", (keyword.lower(),))
    kw_id = cur.fetchall()[0][0]

    return kw_id

def add_artc_db(article):
    kw = article["keyword"]
    content = article["article"]

    # print("Breakdown for", kw)
    kw_id = get_kw_id(kw)

    sect_i = 0
    for sect in content:
        
        # Insert article sections
        cur.execute("""
            INSERT INTO article_section
            (keyword_id, seq, title)
            VALUES
            (%s, %s, %s)
        """, (kw_id, sect_i, sect))
        db.commit()

        sect_id = cur.lastrowid
        # print(sect_id, sect)

        # Insert paragraphs
        # print(content[sect])
        # print('-' * 20)

        par_i = 0
        for sect_par in content[sect]:
            cur.execute("""
                INSERT INTO sect_paragraph
                (section_id, seq, content, source_url)
                VALUES
                (%s, %s, %s, %s)
            """, (sect_id, par_i, sect_par[0], sect_par[1]["url"]))
            par_i += 1

            db.commit()


        sect_i += 1

if __name__ == '__main__':
    to_add_kws = set([
        "computer architecture",
        "natural language processing",
        "reinforcement learning",
        "case-based reasoning"
    ])
    articles = glob.glob("data/articles/*.json")

    for i,filename in enumerate(articles):
        # print(i, filename)

        with open(filename) as f:
            article = json.load(f)

            # print(i, filename)
            if article["keyword"] in to_add_kws:
                print(i, filename)
                print(json.dumps(list(article["article"].keys()), indent=4))
                add_artc_db(article)
            # exit()


