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

Le but de ce projet est de configurer une borne d'accès Internet afin que tous les clients passent par une connexion anonymisée, par exemple avec TOR[@Tor] ou un VPN [@Vpn]. Ce genre de borne d'accès permettrait, par exemple à un journaliste d'avoir un accès à Internet sûr dans un pays où les lois ne sont pas adaptées.

Pour ce projet nous avons choisi de faire une borne d'accès TOR pour découvrir cette technologie.

# Prérequis

Pour réaliser ce projet, nous avons utilisé 2 machines virtuelles linux, une machine cliente (journaliste) et une machine serveur (access point).  La machine access point doit avoir 2 carte réseau, une connectée à internet et une autre pour le réseau local.

## Machines Virtuelle

- Access Point : Machine GNU/Linux, Ubuntu 18.10
- Client : Machine GNU/Linux, Ubuntu 18.10

Nous avons choisi Ubuntu car c'est distribution très rapide à installer et que nous connaissions déjà.

## Réseau

Le structure du réseau est celle-ci :

![Architecture du réseau](./rsc/network-diagram.png){ width=50% }

## Machine Virtuelle Access Point

La machine virtuelle, faisant office d'Access Point, requiert plus de configuration que la machine client. Les paquets requis sont listés ci-dessous

### Programmes nécessaires

Pour l'access point nous avons besoin d'installer Tor [@SetupTor] et Privoxy [@Schaefer]

- privoxy
- tor

```sh
apt-get update
apt-get upgrade
apt-get install tor privoxy -y
```

### Cartes réseau

Voici la configuration nécessaire pour les 2 cartes réseaux dans VirtualBox.

#### Carte connectée à Internet

**Mode :** NAT
**IP :** Automatique

Le réseau de la HE-Arc n'autorise pas les connexions aux réseaux TOR, nous avons utilisé une connexion 4G via un téléphone portable.


#### Carte connectée au réseau local

**Mode :** Internal Network (réseau des machines virtuelles)
**IP :** 192.168.1.1


## Machine Virtuelle Client

Cette section présente les programmes pour la configuration du client et la configuration réseau VirtualBox pour le bon fonctionnement de la machine virtuelle cliente.

### Programmes nécessaires

Le client ne nécessite pas d'installation nécessaire, nous avons uniquement besoin d'un navigateur. Firefox étant installé par défaut, il ne faut rien installer.

### Cartes réseau

Voici la configuration dans VirtualBox de la carte réseau du client.

**Mode :** NAT
**IP :** 192.168.1.2

# Réalisation

La majeur partie du travail a été de configurer l'access point et que tous les services démarrent au démarrage de la machine

## Access Point

La première étape de ce travail a été de configurer la carte réseau de l'access point, privoxy et TOR pour que les services démarrent et que l'utilisateur n'ait pas à devoir savoir configurer l'access point.

### Script de configuration

La configuration de ce programme étant assez complexe, nous avons pris comme référence la configuration qui nous a été transmise par notre professeur par mail, [@Schaefer]. Ensuite nous avons fait un `diff` pour voir quelles lignes étaient différentes par rapport au fichier de base pour intégrer à notre config par défaut (> pour les lignes ajoutés par Monsieur Schaefer et < pour les lignes retirés). Nous avons adapter les lignes nécessaires pour notre configuration. Nous avons également ajouté au le lancement au démarrage des services avec `systemctl`.


**Diff entre la configuration de base et celle de Monsieur Schaefer**
```
> admin-address admin@alphanet.ch
8d8
< filterfile user.filter      # User customizations
9a10,11
> debug      1 # Log the destination for each request Privoxy let through.
> hostname 192.168.99.105
11c13
< listen-address  [::1]:8118
---
> listen-address  192.168.99.105:8118
16a19,24
> permit-access   192.168.1.0/24
> permit-access   127.0.0.1/32
> permit-access   [::1]/128
> permit-access   192.168.99.105/32
> permit-access   192.168.99.104/32
> permit-access   192.168.99.121/32
18c26
< enable-proxy-authentication-forwarding 0
---
> forward-socks5   /               127.0.0.1:9050 .
24d31
< tolerate-pipelining 1
25a33
> handle-as-empty-doc-returns-ok 1
```

**Script de configruation utilisé pour notre proxy**
```shell
sudo su
apt-get update
apt-get upgrade
apt-get install tor privoxy -y
echo "SocksPort 9050
SocksListenAddress 127.0.0.1
Log info file /var/log/tor/notices.log" > /etc/tor/torrc

echo "user-manual /usr/share/doc/privoxy/user-manual
confdir /etc/privoxy
logdir /var/log/privoxy
actionsfile match-all.action
actionsfile default.action
actionsfile user.action
filterfile default.filter
filterfile user.filter
debug   1
logfile logfile
listen-address  127.0.0.1:3128
listen-address  [::1]:3128
listen-address  192.168.1.1:3128
toggle  1
enable-remote-toggle  0
enable-remote-http-toggle  0
enable-edit-actions 0
enforce-blocks 0
buffer-limit 4096
enable-proxy-authentication-forwarding 0
forwarded-connect-retries  0
accept-intercepted-requests 0
allow-cgi-request-crunching 0
split-large-forms 0
keep-alive-timeout 5
tolerate-pipelining 1
socket-timeout 300
forward-socks5 / localhost:9050 .
" > /etc/privoxy/config

systemctl enable tor privoxy
systemctl restart tor privoxy
exit
```

### Configuration réseau

Pour l'access point il ne faut rien changer. Il faut juste que l'adresse IP du gateway soit celle spécifiée précédemment.

## Client

Pour le client, la seule configuration à faire se trouver dans le navigateur et les paramètres.

La configuration de la carte réseau permet de paramètrer l'access point comme gateway.

Nous avons changé le proxy du navigateur et également désactivé le Javascript pour éviter le tracking non-désiré de certains sites.

### Configuration réseau du navigateur.

Pour configurer le navigateur il faut modifier les paramètres de connexion afin qu'elle soit identique à ceci :

![Configuration du proxy](./rsc/configproxypng.png){ width=60% }

Et pour désactiver le navigateur il faut taper `about:config` dans la barre d'adresse et changer la valeur à `false` comme sur l'image ci-dessous

![Désactivation javascript](./rsc/js.png){ width=80% }

Nous avons vérifié que le javascript ait bien été désactivé en allant sur facebook, on peut voir le paramètre "noscript" s'afficher dans la barre d'adresse du navigateur. Il est dû a une redirection qui se produit lorsqu'il remarque que nous n'utilisons pas javascript.

![Vérification désactivation du javascript](./rsc/js2.png){ width=80% }

### Configuration de la carte réseau

Il faut configurer la carte réseau pour que la gateway soit l'access point

![Gateway](./rsc/gateway.png){ width=60% }

\newpage

# Contrôles

Pour vérifier si le fonctionnement de notre configuration Tor a fonctionné. Nous avons utiliser le vérificateur Tor du site officiel[@CheckTorProject].

![Vérifications](./rsc/congrat_tor.png){ width=60% }

Nous avons également regarder où était notre noeud de sortie, avec  [cmyip](https://cmyip.com)

![Cmyip ?](./rsc/cmyip.png){ width=60% }

# Risques persistant

Si la personne n'est pas proprement sensibilisée, elle risque d'avoir un comportement qui puisse compromettre son anonymat. Il font dont que l'utilisateur ait connaissance de certaines pratique comme ne jamais posté d'informations personnelles en étant sur le terrain. Pour plus d'information, il peut aller voir ces deux références [@BonnesPratiquesTor] et [@BonnesPratiquesStackEchange].

D'autres pratiques que nous avons retenues :
- Ne pas ouvrir de document style DOC / PDF télécharger dans le Tor.
- Utiliser les versions HTTPS des sites quand disponibles.
- Faire régulièrement les mises à jour de la machine utilisé.

# Conclusion

Pour conclure, le projet c'est déroulé sans gros problème, certaines configurationes n'étaient pas évidentes, mais avec l'aide de M. Schaefer et quelques recherches sur Internet, les problèmes ont été résolus. Finalement, la machine virtuelle fonctionne et les services se lancent au démarrage sans que l'utilisateur n'ait à se connecter à l'Access Point. Par contre, il devra quand même changer ses paramètres réseaux et la configuration du navigateur.

\newpage

\listoffigures

# References

