#!/usr/bin/env python3

import sys
import json

sys.stderr.write("Preprocessor started.\n")

def process_chapter(chapter, snippets):
    content = ''
    if 'Chapter' in chapter.keys():
        content = chapter['Chapter']['content']
    else:
        return chapter
    for placeholder, html in snippets.items():
        content = content.replace(placeholder, html)
    chapter['Chapter']['content'] = content
    return chapter

def main():
    if len(sys.argv) > 1: # we check if we received any argument
        if sys.argv[1] == "supports": 
            # then we are good to return an exit status code of 0, since the other argument will just be the renderer's name
            sys.exit(0)

    input_data = json.load(sys.stdin)
    snippets = {
        "{{reusable_html_snippet}}": "<div class='my-html-snippet'>This is reusable HTML</div>",
        "{{another_snippet}}": "<p>Another snippet content</p>",
    }
    book = input_data[1]
    book["sections"] = [process_chapter(section, snippets) for section in book["sections"]]
    json.dump(book, sys.stdout)

if __name__ == "__main__":
    main()
