---
layout: about
title: About
permalink: /
subtitle: "The AI x Software Engineering & Testing Lab<br>School of Computer Science, University of Sheffield"

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

## News

{% include news.liquid limit=true %}


## Recent Papers

<div class="publications">
  {% bibliography --group_by none --max 5 %}
</div>
