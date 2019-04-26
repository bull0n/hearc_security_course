---
title: Access Point Tor
subtitle: Rapport
lang: fr
author:
- Bulloni Lucas <lucas.bulloni@he-arc.ch>
- Margueron Raphaël <raphael.margueron@he-arc.ch>
date: \today
pagesize: A4
numbersections: true
documentclass: scrartcl
geometry: margin=2.5cm
bibliography: rapport.bib
header-includes: |
      \usepackage{fancyhdr}
      \pagestyle{fancy}
      \fancyhead[R]{Lucas Bulloni \& Raphael Margueron}
      \usepackage{float}
      \floatplacement{figure}{H}
---

\newpage

\tableofcontents

\newpage

# Introduction

Le but de ce projet est de configuré une borne d'accès Internet afin que tous les clients passent par une connexion anonymisée, par exemple avec TOR ou un VPN. Ce genre de borne d'accès permettrait, par exemple à un journaliste d'avoir un accès à Internet sûr dans un pays où les lois ne sont pas adaptés.

Pour ce projet nous avons choisi de faire une borne d'accès TOR pour découvrir cette technologie.

# Configuration

Pour réaliser ce projet, nous avons utilisé 2 machines virtuelles linux, une client et une serveur.  La machine access point doit avoir 2 carte réseau, une connecté à internet et une autre pour le réseau locale

## Machines Virtuelle

- Access Point : Machine GNU/Linux, Ubuntu 18.10
- Client : Machine GNU/nLinux, Ubuntu 18.10

## Réseau

Le structure du réseau est celle-ci : 

![Architecture du réseau](./rsc/network-diagram.png){ width=50% }

## Machine Virtuelle Access Point

### Programmes nécessaires

### Cartes réseau

## Machine Virtuelle Client

### Programmes nécessaires

### Cartes réseau

# Réalisation

bonjour

# Conclusion

bonjour

\newpage

\listoffigures

# References
