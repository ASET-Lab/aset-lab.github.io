---
layout: about
title: About
permalink: /
subtitle: "The AI x Software Engineering & Testing Lab<br><a href='https://sheffield.ac.uk/cs'>School of Computer Science</a>, <a href='https://sheffield.ac.uk/'>University of Sheffield</a>"

selected_papers: false # includes a list of papers marked as "selected={true}"
social: true # includes social icons at the bottom of the page

announcements:
  enabled: false # includes a list of news items
  scrollable: true # adds a vertical scroll bar if there are more than 3 news items
  limit: 3 # leave blank to include all the news in the `_news` folder

latest_posts:
  enabled: false
  scrollable: true # adds a vertical scroll bar if there are more than 3 new posts items
  limit: 3 # leave blank to include all the blog posts
---

<style>
  /* Homepage heading and subtitle (the about layout has no _styles support) */
  .post-header .post-title { font-weight: 700; }
  .post-header .desc { font-weight: 700; font-size: 1.25rem; line-height: 1.4; }
</style>


We develop and evaluate practical software engineering techniques to support the efficient development of robust, maintainable software and cyber-physical systems. 

Much of our research is geared towards the growing role of AI in the software-development lifecycle, from agentic software development through to systems such as autonomous vehicles that themselves incorporate AI into their core functionality.

<div class="d-flex flex-wrap" style="gap: 1rem;">
  <div style="flex: 1 1 0; min-width: 150px;">
    {% include figure.liquid loading="eager" path="assets/img/aset_icst_26.png" class="img-fluid rounded z-depth-1" alt="Members of the ASET group at ICST'26" caption="Members of the ASET group at ICST'26" %}
  </div>
  <div style="flex: 2.32 1 0; min-width: 250px;">
    {% include figure.liquid loading="eager" path="assets/img/aset_home_picture.jpg" class="img-fluid rounded z-depth-1" alt="ASET members on their annual walk in the Peak District" caption="ASET members out on their annual walk in the beautiful Peak District" cache_bust=true %}
  </div>
</div>

{% for pair in site.data.coauthors %}{% assign member = pair[1].first %}{% if member.head_of_group %}{% assign head_email = member.email %}{% endif %}{% endfor %}

### Working with practitioners

Our goal is to develop solutions that address significant Software Engineering and Testing challenges. As such we are always keen to work with industrial partners in the tech community to develop novel solutions that will make an impact. Collaborations can take on a variety of shapes and sizes, from short-term student projects to Ph.D. studentships or more formal collaborative research projects. If you are interested in working with us, please [contact us](mailto:{{ head_email }})!

## News

{% include news.liquid limit=true %}


## Recent Papers

<div class="publications">
  {% bibliography --group_by none --max 5 %}
</div>
