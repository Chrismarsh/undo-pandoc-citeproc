After discussion with [@mbroedl](https://github.com/mbroedl/invert-pandoc-docx) on this [pandoc-citeproc](https://github.com/jgm/pandoc-citeproc/issues/323) ticket, this attempts to invert the citeproc references so-as to allow for easily converting docx back to markdown.

This supports a workflow of Markdown -> docx -> Markdown. Often the case when co-authors use docx, but the manuscript is written with md.

Because there is no clear way to embed meta data into the docx and extract when going docx to md, this wraps every citation in an Emph section. This allows for finding Emph sections with links that match the citeproc format, thus allowing for delimiting the citation area. This approach allows for diacritics in author names. 

Further, it writes out meta data to `citations.txt`. This allows for saving the prefix and suffix, as well as citation type so as to easily reinsert this. For example:

```verne1870twenty;;;NormalCitation
adams1992mostly;see;;NormalCitation
verne1870twenty;e.g.;;NormalCitation
adams1992mostly;cf.;or so;NormalCitation
adams1992mostly;;, page 10;NormalCitation
verne1870twenty;;, notes 20-25;NormalCitation
```

If this file isn't present, then '(' and ')' are used to try to guess if it is a Normal citation or an inline citation. This will only work for author-year in-text style citations (e.g., Marsh et al (2018)).

This approach relies on converting md->docx using the `-M link-citations` flag. This preseves the initial citation key and without this, this cannot work.