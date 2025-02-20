from src.syllabizer import check
from glob import glob

if __name__ == "__main__":
    verses = [
        (1,1,1,2,1),
        (1,1,1,1,1,1,1),
        (1,1,1,1),
        (1,1,1,1,1,1,1,1),
        (1,1,2,1,1,1,1),
        (1,1,1,1,1,1,1),
        (1,1,2,1,1,2),
        (2,1,1,2),
        (2,1,1,1,1),
    ]
    for v in range(len(verses)):
        with open(f"verse{v+1}.csv", "w") as f:
            f.write("Verse,File,Excerpt\n")
            f.flush()
            for file in glob("./*.txt"):
                for verse, line in check(file, verses[v], permissible_skips=0):
                    f.write(f"{verse},{file},{line.replace(",", ".")}\n")
                f.flush()

