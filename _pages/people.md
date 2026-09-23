---
layout: page
permalink: /people/
title: People
nav: true
nav_order: 5
_styles: >
  .post-header { display: none; }
---


<section class="our-webcoderskull">
<div class="container-fluid">
  {% assign current_role = "" %}

  {% for pair in site.data.coauthors %}
    {% assign member = pair[1].first %}
    {% if member.role %}
      {% if member.role != current_role %}
        {% if current_role != "" %}</ul>{% endif %}
        {% assign current_role = member.role %}
        <h3 class="text-left mb-1" style="margin-bottom: 0.5rem;">{{ member.role }}</h3>
        <ul class="row mb-0" style="margin-bottom: 1rem !important;">
      {% endif %}

      {% assign display_name = member.firstname.first | append: " " | append: member.lastname %}
      {% if member.title %}{% assign full_name = member.title | append: " " | append: display_name %}{% else %}{% assign full_name = display_name %}{% endif %}
      <div class="col-12 col-md-3 col-lg-3 mb-2">
        <div class="cnt-block equal-hight" style="padding: 15px 10px; margin-bottom: 0;">
          <div style="text-align: center;">
            {% if member.img %}
              {% if member.url %}
                <a href="{{ member.url }}" target="_blank" rel="noopener">
                  <img src="{{ member.img }}" class="img-fluid z-depth-1 rounded" style="aspect-ratio: 1 / 1; object-fit: contain;" loading="eager" alt="{{ full_name }}">
                </a>
              {% else %}
                <img src="{{ member.img }}" class="img-fluid z-depth-1 rounded" style="aspect-ratio: 1 / 1; object-fit: contain;" loading="eager" alt="{{ full_name }}">
              {% endif %}
            {% else %}
              <div class="z-depth-1 rounded" style="aspect-ratio: 1 / 1; background: rgba(128, 128, 128, 0.18);"></div>
            {% endif %}
          </div>
          <div style="text-align: center; margin-top: 0.5rem;">
            <h6>
              {% if member.url %}<a href="{{ member.url }}" target="_blank" rel="noopener" style="text-decoration: none;">{{ full_name }}</a>{% else %}<span style="color: var(--global-text-color);">{{ full_name }}</span>{% endif %}
            </h6>
            {% if member.head_of_group %}<div class="text-muted" style="font-size: 0.85rem; margin-top: -0.35rem;">(Head of group)</div>{% endif %}
          </div>
        </div>
      </div>
    {% endif %}
  {% endfor %}
  {% if current_role != "" %}</ul>{% endif %}
</div>
</section>