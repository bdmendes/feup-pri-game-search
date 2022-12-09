import sys
import pandas as pd
import os

languages_column = 'SupportedLanguages'
audio_languages_column = 'SupportedAudioLanguages'


def split_languages(languages, is_audio=False):
    languages = languages.split(' ')
    i = 0
    while i < len(languages):
        if (is_audio and '*' not in languages[i]) or len(languages[i]) == 0 or languages[i][0].islower():
            del languages[i]
            i -= 1
        else:
            languages[i] = languages[i].split('*')[0].strip()
            if languages[i] == '':
                del languages[i]
                i -= 1
            elif languages[i] == 'Traditional' or languages[i] == 'Simplified':
                languages[i] = languages[i] + ' Chinese'
                del languages[i + 1]
                i -= 1
        i += 1
    return languages


def main():
    arg = os.path.dirname(__file__) + '/' + sys.argv[1]

    data = pd.read_csv(arg)

    data[audio_languages_column] = data[languages_column].apply(
        lambda x: split_languages(x, True))
    data[languages_column] = data[languages_column].apply(split_languages)

    data.to_csv(arg, index=False)


if __name__ == "__main__":
    main()
    print("Parsed languages")
