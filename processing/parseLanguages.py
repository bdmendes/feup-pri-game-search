import sys
import pandas as pd
import os


def main():
    arg = os.path.dirname(__file__) + '/' + sys.argv[1]

    data = pd.read_csv(arg)

    languages_column = 'SupportedLanguages'
    audio_languages_column = 'SupportedAudioLanguages'
    audio_languages_column_data = []
    languages_column_data = []

    for i in range(data.shape[0]):
        new_language_data = list(data.iloc[i][languages_column].split(' '))
        new_audio_language_data = []
        extra = ""

        for i, language in enumerate(new_language_data):
            if language == '':
                continue

            if language == 'Traditional' or language == 'Simplified':
                extra = language + ' '
                continue

            if '*' == language[-1] or language.count('**') == 1:
                new_language_data[i] = extra + language[:-1]
                new_audio_language_data.append(extra + language[:-1])
                extra = ''

        if new_audio_language_data != []:
            new_language_data = new_language_data[:-4]
            new_language_data[-1] = new_language_data[-1].split('*')[0]
            new_audio_language_data[-1] = new_audio_language_data[-1].split('*')[
                0]

        audio_languages_column_data.append(new_audio_language_data)
        languages_column_data.append(new_language_data)

    data[audio_languages_column] = audio_languages_column_data
    data[languages_column] = languages_column_data

    data.to_csv(arg, index=False)


if __name__ == "__main__":
    main()
    print("Parsed languages")
