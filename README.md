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

`*.toml` files have the following format as described by the [TOML v1.0.0 specification](https://toml.io/en/):

```toml
# Comments are prepended with a '#' character.

# Configuration is split into [section]s.

[String]
literal = 'unescaped\tline\tWYSIWYG'
singleline = "this is a new line"
multiline = """
\b      - backspace         (U+0008)
\t      - tab               (U+0009)
\n      - linefeed          (U+000A)
\f      - form feed         (U+000C)
\r      - carriage return   (U+000D)
\"      - quote             (U+0022)
\u1234  - unicode           (U+1234)
"""

[Number]
int1 = +5349221
int2 = -5_3_49_221
hex1 = 0xDEADBEEF
oct1 = 0o01234567
fp1  = +6.626e-34
fp2  = 224_617.445_991_228
sf1  = -inf # negative infinity
sf2  = +inf # positive infinity
sf3  = +nan # not a number

[DateTime]
ld1 = 1979-05-27  # Local Date
lt1 = 07:32:00    # Local Time
ldt1 = 1979-05-27T07:32:00   # Local Date-Time
odt1 = 1979-05-27T07:32:00Z  # Offset Date-Time

[Structures]
array = [[1, 2], ["a", "b", "c"]]
inlineTable = [
    { x = 1, y = 2, z = 3 },
    { x = 4, y = 5, z = 6 },
    { x = 7, y = 8, z = 9 },
]

# Double-bracketed sections are called arrays and can be used multiple times.

[[Array]]
name = "Array 1"

[[Array]]
name = "Array 2"

```

## MongoDB

The scripts were written to ingest files into our MongoDB instance. We maintain a privately hosted MongoDB server running alongside a BI Connector middleware.

MongoDB's NoSQL database meant we could ingest only the data we needed to for particular service providers and could flexibly change our schema as needed.

The BI Connector allowed us a SQL-like layer to interface with when using Power BI. The middleware, created by the MongoDB team, scans our collections to automatically generate a flat, tabluar structure that can be understood in a SQL context. The middleware exposes an end point over a network port accessible by any ODBC-driver compliant frontend.

In this case, we used Power BI to create the visualizations from our work.

## Data

The repository's `data/` folder served as a media datalake - data is stored in a largely unstructured format and we wrote scripts to process and tidy data for our end requirements.

Different service provider files were created and scripts were written to extract similar features for the purposes of classification and ingestion to MongoDB.

```yaml
_id: <ObjectId>
facility: <str>
keywords: [<str>,...]
category: 
  disability: [<str>,...]
  service: [<str>,...]
info:
  website: <subdomain.domain.com>
  fax: <XXX-XXX-XXXX>
  phone: <XXX-XXX-XXXX>
  addressee: <entity>
address:
  street:
    line1: <str>
    line2: <str>
  city: <city>
  county: <county>
  state: <state>
  zipcode: <zipcode>
```
