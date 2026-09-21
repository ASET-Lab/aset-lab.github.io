---
layout: about
title: About
permalink: /
subtitle: "The AI x Software Engineering & Testing Lab<br>School of Computer Science, University of Sheffield"

profile:
  align: right
  image: aset_home_picture.jpg
  image_circular: false # crops the image to make it circular
  more_info: >

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

## News

{% include news.liquid limit=true %}


## Recent Papers

<div class="publications">
  {% bibliography --group_by none --max 5 %}
</div>
