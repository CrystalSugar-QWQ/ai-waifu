def generate_subtitle(text, file):
    # output.txt will be used to display the subtitle on OBS
    with open(file, "w", encoding="utf-8") as outfile:
        try:
            text = text
            words = text.split()
            lines = [words[i:i+10] for i in range(0, len(words), 10)]
            for line in lines:
                outfile.write(" ".join(line) + "\n")
        except Exception:
            print("Error writing to output.txt")


def clear_subtitle(file):
    with open(file, "w") as f:
        f.truncate(0)