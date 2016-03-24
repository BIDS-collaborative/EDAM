# EDAM

Ecostations Data Access Monitor

Join us for discussions on [![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/BIDS-collaborative/EDAM?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) .

Learn more about current status of this project on our [wiki](../../wiki).

## origins

This proposal originated at a meeting with Neil Davies (Moorea IDEA, BIDS), Jorrit Poelen (GloBI, author of this text) and Charlotte Cabasse (BIDS) at BIDS on Aug 5, 2015.

## title

(Island) Ecostations Data Access Monitor (EDAM) - Phase 1 - species lists, food webs and associated citations.

## purpose

Develop methods to openly compare ecological data richness /completeness of (Island) Ecostations to promote open data and tool re-use between researchers, citizen scientists, educators, foundations and regulatory bodies.

## setting

Student project for BIDS Hacking Measurement Class Fall 2015: http://www.ischool.berkeley.edu/courses/i290-hm.

## introduction

As large biodiversity collections and environmental data are accessible online,
global research communities have an unprecedented access to (siloed) datasets.
Now that methods are within reach that allow to combine and process
biodiversity data at global scales, institutions can start to re-examine
existing data to coordinate data collection efforts, evolve data sharing
strategies and discover methods to efficiently sustain our (island) ecosystems.
A first step toward integrating the data is to provide a side-by-side
comparison of existing data associated with active island ecostation
communities to stimulate knowledge sharing and collaboration. See [Meyer et al. 2015](http://dx.doi.org/10.1038/ncomms9221) for a recent discussion about the importance of identifying "[...] Gaps in digital accessible information (DAI)[...]" or biodiversity data completeness. 

## methods

Ecostation biodiversity data summaries are derived from openly available
biodiversity data repositories (e.g. GBIF, iDigBio, GloBI). Initially only
species lists and associated food webs are compiled for participating
ecostations using automated data processing algorithms. For each ecostation,
the completeness of the lists and webs are estimated. Also, the similarity of
the lists and webs are calculated across the spatially separated island
ecosystems to highlight ecological likeness.  By providing EDAM, spatially and
institutionally disjointed projects now have a data- driven method to see how
much ecological data is available for specific spatio- taxonomic spaces. We
hope that comparing available ecological data across ecostations will help
stimulate collaboration between scientists, technologists, educators, local
governments and research foundations to help better understand and sustain
ecosystems around us.

## goals

In order to archieve EDAM Phase I, we need to:

 1. (scope) identify 3-5 island ecostations (e.g. Moorea/Oahu/Friday
    Harbor/Galápagos)
 2. (scope) define/identify spatial and taxonomic ranges for ecostations
 3. (data) generate/retrieve spatio-taxonomic species checklist at scale and
    on- demand (e.g.https://github.com/jhpoelen/effechecka, Map of Life
    mol.org)
 4. (data) construct local biotic interaction webs based on species interaction
    data and spatially explicit checklist: occurrence + interaction = local
    biotic interaction web estimate.
 5. (model, analysis) develop/adopt similarity measures for checklists and
    biotic interaction webs
 6. (model, analysis) develop/adopt completeness measures for checklists and
    biotic interaction webs
 7. (share) create a web-accessible visualization to make results (and
    associated data sources) easy to access.

## realization

Given the availability of relevant ecolological data and the limited scope of
needed data processing capabilities, a first prototype of EDAM Phase I is
estimated to take 2-3 months for a group of digitally literate graduate
students with an allocation of ~10 hrs a week. The outcome of this project will
help define future funding to further develop advanced phases of the EDAM
project.

## contact

Jorrit Poelen, http://globalbioticinteractions.org, https://github.com/jhpoelen
or jhpoelen at xs4all dot nl
