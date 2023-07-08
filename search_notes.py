def search_notes():
    keyword = input('Enter a keyword to search: ')
    found_notes = []

    with open('notes.txt', 'r') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            if lines[i].startswith('Title:') and keyword.lower() in lines[i].lower():
                title = lines[i][7:].strip()
                content = lines[i+1][6:].strip()
                note = {'title': title, 'content': content}
                found_notes.append(note)
                i += 2
            else:
                i += 1

    if found_notes:
        print('Found notes:')
        for note in found_notes:
            print(f"Title: {note['title']}")
            print(f"Text: {note['content']}")
            print()
    else:
        print('No notes found.')


if __name__ == "__main__":
    search_notes()
