def generate_subtitle(text, file):
    # output.txt will be used to display the subtitle on OBS
    with open(file, "w", encoding="utf-8") as outfile:
        try:
            outfile.write(text)
        except Exception:
            print(f"Error writing to {file}")


def clear_subtitle(file):
    with open(file, "w") as f:
        f.truncate(0)