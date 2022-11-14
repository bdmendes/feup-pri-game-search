FROM solr:8.10

COPY data/processed.json /data/processed.json

COPY data/schema.json /data/schema.json

COPY helper_scripts/startup.sh /scripts/startup.sh

ENTRYPOINT ["/scripts/startup.sh"]