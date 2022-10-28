# Information retrieval

Information retrieval using Apache Solr.

## How to use

- Use Docker to fire up a Solr instance: `docker run --name pri_solr -p 8983:8983 solr:8.10`.
- Create a collection for the games: `docker exec pri_solr bin/solr create_core -c games`.
- Update the schema with a POST request to `http://localhost:8983/solr/games/schema`, passing the indexing and query schema in the body, and `Content-type:application/json` in the header.
- Update the collection with a POST request to `http://localhost:8983/solr/games/update?commit=true`, passing the `processed.csv` dataset in the body, and `Content-type:text/csv` in the header.
- Use the Apache Solr interface to perform queries and evaluate them.

> If you update the schema after you feed the collection with data, changes won't reflect. The easiest way to fix this is to delete the core and start over: `docker exec pri_solr bin/solr delete -c games`.

## Schema

TBD

## Queries

TBD