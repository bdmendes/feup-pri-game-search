PYTHON = python

all: download process

download:
	curl -L -o data/original.csv https://query.data.world/s/dtnoot72bcs7smp535vclrfaj5n3ut

process: combine_categories combine_descriptions delete_outliers

combine_categories:
	$(PYTHON) processing/combine_categories.py

combine_descriptions:
	$(PYTHON) processing/combine_descriptions.py

delete_outliers:
	$(PYTHON) processing/delete_outliers.py

.PHONY: clean
clean:
	rm -f data/original.csv