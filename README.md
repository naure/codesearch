# Code Search

A code search engine that actually analyzes and follows the code.

It finds lines of code based on a query, then builds complete snippets
by adding the dependencies and dependents of that code, for instance keeping
variable declarations and usages together.

Searching for a function name will show several examples of usage. The
code snippets are (mostly) valid and ready to be copy-pasted. They include imports and
constants, show where parameters are typically taken from, and what can be
done with the output of the function. Relevant parts are color-coded,
and more code can be digged out on demand.

## Examples

Let's search for *http response*. We get example snippets generated dynamically. They contain the necessary dependencies in blue - here the imports of *HttpResponse* and *json*, and the *out* variable.

We can also follow the impact of this statement in red: for example *return response*, then a call to this particular function.

![](pic/example_django.png?raw=true "Search Results")


The "More" buttons can expand the snippets further if necessary to understand or reuse the snippet:

![](pic/request_1.png?raw=true "Minimal Snippet")

![](pic/request_2.png?raw=true "Developed Snippet")

## How it works

The source code is analyzed using a parser, extracting data from ASTs, honoring the scoping rules to find dependencies and impacts, and loading the results into a graph database.

The search engine finds statements and walks the graph from there.

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
