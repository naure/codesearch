# Code Search

A code search engine that actually analyzes and follows the code.

It finds lines of code based on a query, then builds complete snippets
by adding the dependencies and dependents of that code, for instance keeping
variable declarations and usages together.

## Run

The following will install neo4j, nodejs and other tools, and build the project. Assuming an ubuntu server.

Some sample code will then be parsed and loaded into the graph database.

Finally the code can be searched and explored using a django+angular webapp.

    make just_run_everything
    # See Makefile for individual steps

# Status

This was an early experimental project to combine search with static code parsing.
This was also a way to learn more about graphs in Neo4j, Pypy internals, and the absolute minimum of web dev.

# Future

I'm continuing my journey to tap into the immeasurable knowledge contained in open source code, with new ideas and
more advanced search and NLP techniques at http://deckard.ai.
