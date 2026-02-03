---
layout: page
title: projects
permalink: /projects/
description: A selection of visualization projects, from research prototypes to applied systems.
nav: true
nav_order: 3
display_categories: [research, applied]
horizontal: false
---

<!-- pages/projects.md -->
<div class="projects">
{% if site.enable_project_categories and page.display_categories %}
  {% for category in page.display_categories %}
  <a id="{{ category }}" href=".#{{ category }}">
    <h2 class="category">{{ category }}</h2>
  </a>
  {% assign categorized_projects = site.projects | where: "category", category %}
  {% assign sorted_projects = categorized_projects | sort: "importance" %}

{% if page.horizontal %}

  <div class="container">
    <div class="row row-cols-1 row-cols-md-2">
    {% for project in sorted_projects %}
      {% include projects_horizontal.liquid %}
    {% endfor %}
    </div>
  </div>
  {% else %}
  <div class="row row-cols-1 row-cols-md-3">
    {% for project in sorted_projects %}
      {% include projects.liquid %}
    {% endfor %}
  </div>
  {% endif %}
  {% endfor %}
{% else %}
{% assign sorted_projects = site.projects | sort: "importance" %}
  {% if page.horizontal %}
  <div class="container">
    <div class="row row-cols-1 row-cols-md-2">
    {% for project in sorted_projects %}
      {% include projects_horizontal.liquid %}
    {% endfor %}
    </div>
  </div>
  {% else %}
  <div class="row row-cols-1 row-cols-md-3">
    {% for project in sorted_projects %}
      {% include projects.liquid %}
    {% endfor %}
  </div>
  {% endif %}
{% endif %}
</div>

## Archive

Additional projects and experiments from previous years:

- **ConceptLights** - [demo](https://exploreat.acdh-dev.oeaw.ac.at/exploreAT-conceptlights/), [paper](https://dh2018.adho.org/shedding-light-on-indigenous-knowledge-concepts-and-world-perception-through-visual-analysis/)
- **SoccerVis** - work-in-progress visual analytics system for soccer analysis
- **D3 tutorial (in Spanish)** - [notebook](https://observablehq.com/@ale0xb/d3-tutorial), [post](https://twitter.com/alexbensan/status/1201833512413863936)
- **Rural Schools in Castilla y Leon** - [demo](https://bl.ocks.org/ale0xb/dac7e1086663f23a471864b21fbea5b9)
- **Overrepresentation in the Electoral System in Spain** - [demo](https://bl.ocks.org/ale0xb/2b8eb65eb5e3b6420ca1e67aec93ddef)
- **Topography of Concepts** - exploratory visualization for lexicographic data
- **Visualization of TCD's 1641 Depositions Dataset** - [code](https://github.com/providedh/1641-depositions-vis)
- **Inter-Concept Relationships in a Chord Diagram** - exploratory visualization built in the exploreAT! context
- **Internal Migrations in Spain (2016)** - [demo](http://bl.ocks.org/ale0xb/ef5837f83edf937ece94a2665d60e5a3)
