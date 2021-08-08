# ISTE 612 - Term Project

Term project repository for ISTE 612.

## Project Structure

This repository contains various scripts that were used to preprocess and tidy data prior to ingestion with MongoDB. Each folder is a general attempt to organize scripts and Jupyter notebooks by topic.

The `data/` folder contains the data we're working with.
The `classifier/` folder contains work related to the clustering algorithm.
The `ingestion/` folder contains scripts used to help ingest data into MongoDB.
The `scraper/` folder contains a series of scripts used to scrape websites of their data.

Generally we used a range of tools, including:

- `pandas`
- `numpy`
- `scikit-learn`
- `scrapy`

## Configuration

Configuration settings are located in `*.toml` files and processed using `dynaconf`.

A `.secrets.toml` file is expected to contain database authentication settings. This is not included with the repository, but you can create a `.secrets.toml` file alongside `settings.toml` with the appropriate settings.

## MongoDB

The scripts were written to ingest files into our MongoDB instance. We maintain a privately hosted MongoDB server running alongside a BI Connector middleware.

MongoDB's NoSQL database meant we could ingest only the data we needed to for particular service providers and could flexibly change our schema as needed.

The BI Connector allowed us a SQL-like layer to interface with when using Power BI. The middleware, created by the MongoDB team, scans our collections to automatically generate a flat, tabluar structure that can be understood in a SQL context. The middleware exposes an end point over a network port accessible by any ODBC-driver compliant frontend.

In this case, we used Power BI to create the visualizations from our work.

## Data

The repository's `data/` folder served as a media datalake - data is stored in a largely unstructured format and we wrote scripts to process and tidy data for our end requirements.

Different service provider files were created and scripts were written to extract similar features for the purposes of classification and ingestion to MongoDB.

```yaml
facility: <str>
info:
  phone: [<XXX-XXX-XXXX>,...]
  fax: [<XXX-XXX-XXXX>,...]
  website: <subdomain.domain.com>
  person: <entity>
keywords: [<str>,...]
address:
  street:
    line_1: <str>
    line_2: <str>
  city: <city>
  county: <county>
  state: <state>
  zipcode: <zipcode>
category: 
  disability: [<str>,...]
  service: [<str>,...]
misc: 
  content: [<str>,...]
  <key>: <value>
```
