---
layout: page
title: Software
permalink: /software/
nav: true
nav_order: 4
description: Software developed by the lab, openly available under permissive licenses.
---

We routinely develop software systems to experiment with and evaluate the techniques we develop, and our software is openly available with permissive licensing. 
We are keen to support uptake by practitioners. If you would like support with the software, please feel free to use the issue trackers in the attached GitHub repositories, or contact the researchers listed below.

---

### Causal Testing Framework

A framework for testing causal relationships in hard-to-test systems such as cyber-physical systems and computational models.

**License:** MIT — **Contacts:** [Michael Foster]({{ site.data.coauthors.foster[0].url }}), [Neil Walkinshaw]({{ site.data.coauthors.walkinshaw[0].url }})

<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% include repository/repo.liquid repository="CITCOM-project/CausalTestingFramework" %}
</div>

---

### CAWSR (Carla Autoware Scenario Runner)

A scenario execution engine built for the testing of Autoware in CARLA on route-based scenarios.

**License:** MIT — **Contacts:** [Olek Osikowicz]({{ site.data.coauthors.osikowicz[0].url }}), [Donghwan Shin]({{ site.data.coauthors.shin[0].url }})

<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% include repository/repo.liquid repository="Intelligent-Testing-Lab/cawsr" %}
</div>

---

### DT-Drive

A tool for removing flakiness from tests of autonomous driving systems in the CARLA framework.

**License:** MIT — **Contacts:** [Sanjeetha Pennada]({{ site.data.coauthors.pennada[0].url }}), [Donghwan Shin]({{ site.data.coauthors.shin[0].url }})

<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% include repository/repo.liquid repository="SanjeethaPennada/DT-DRIVE" %}
</div>

---

### Multiplex

A tool for prototyping and comparing LLM-based mutation testing approaches.

**License:** MIT — **Contacts:** [Megan Maton]({{ site.data.coauthors.maton[0].url }}){% if site.data.coauthors.mcminn[0].url %} and [Phil McMinn]({{ site.data.coauthors.mcminn[0].url }}){% else %} and Phil McMinn{% endif %}

<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% include repository/repo.liquid repository="LLM-Mutation/multiplex" %}
</div>

---

### Mutest-rs

A mutation testing framework for Rust.

**Main website:** [mutest.rs](https://mutest.rs/) · **License:** Apache 2.0 — **Contacts:** [Zálan Lévai]({{ site.data.coauthors.levai[0].url }}), [Donghwan Shin]({{ site.data.coauthors.shin[0].url }}){% if site.data.coauthors.mcminn[0].url %}, [Phil McMinn]({{ site.data.coauthors.mcminn[0].url }}){% else %}, Phil McMinn{% endif %}

<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% include repository/repo.liquid repository="zalanlevai/mutest-rs" %}
</div>

---

### PseudoSweep

A framework to identify pseudo-tested statements in Java code.

**License:** MIT — **Contacts:** [Megan Maton]({{ site.data.coauthors.maton[0].url }}){% if site.data.coauthors.mcminn[0].url %} and [Phil McMinn]({{ site.data.coauthors.mcminn[0].url }}){% else %} and Phil McMinn{% endif %}

<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% include repository/repo.liquid repository="PseudoTested/PseudoSweep" %}
</div>

---

### StateChum

A tool for inferring state machine models from system logs. Generalised implementations of our LTS-Diff state machine differencing engine have been developed externally by Dennis Hendricks at TNO ([gLTSdiff](https://github.com/TNO/gLTSdiff)).

**License:** GPL-3.0 — **Contacts:** [Kirill Bogdanov]({{ site.data.coauthors.bogdanov[0].url }})

<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% include repository/repo.liquid repository="kirilluk/statechum" %}
</div>