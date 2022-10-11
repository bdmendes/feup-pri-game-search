PYTHON = python
ORIGINAL_CSV_PATH = data/original.csv
PROCESSED_CSV_PATH = data/processed.csv
PROCESSED_CSV_OUTER_PATH := ../$(PROCESSED_CSV_PATH)

.PHONY: all collect download get_wiki_data process drop_rows drop_columns group_categories group_features group_genres parse_languages clean

all: collect process

collect: download get_wiki_data

download:
	curl -L -o $(ORIGINAL_CSV_PATH) https://query.data.world/s/dtnoot72bcs7smp535vclrfaj5n3ut
	cp $(ORIGINAL_CSV_PATH) $(PROCESSED_CSV_PATH)

get_wiki_data:
	$(PYTHON) collection/getWikiData.py $(PROCESSED_CSV_OUTER_PATH)

process: drop_rows drop_columns group_categories group_features group_genres parse_languages

drop_rows:
	$(PYTHON) processing/dropRepeatedRows.py $(PROCESSED_CSV_OUTER_PATH)

drop_columns:
	$(PYTHON) processing/dropUselessColumns.py $(PROCESSED_CSV_OUTER_PATH)

group_categories:
	$(PYTHON) processing/groupCategories.py $(PROCESSED_CSV_OUTER_PATH)

group_features:
	$(PYTHON) processing/groupFeatures.py $(PROCESSED_CSV_OUTER_PATH)

group_genres:
	$(PYTHON) processing/groupGenres.py $(PROCESSED_CSV_OUTER_PATH)

parse_languages:
	$(PYTHON) processing/parseLanguages.py $(PROCESSED_CSV_OUTER_PATH)

clean:
	rm -f $(ORIGINAL_CSV_PATH)
	rm -f $(PROCESSED_CSV_PATH)